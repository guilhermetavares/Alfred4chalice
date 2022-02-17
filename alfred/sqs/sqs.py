import importlib
import json

import boto3
from botocore.exceptions import ClientError

from alfred.sentry import sentry_sdk
from alfred.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, SQS_QUEUE_URL

from .exceptions import SQSTaskMaxRetriesExceededError

sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

DEFAULT_QUEUE_URL = SQS_QUEUE_URL
DEFAULT_DELAY = 1
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 60 * 3


class SQSTask:
    default_queue_url = DEFAULT_QUEUE_URL
    default_delay = DEFAULT_DELAY
    max_retries = DEFAULT_MAX_RETRIES
    default_retry_delay = DEFAULT_RETRY_DELAY

    def __init__(self, bind=False, retries=0, queue_url=None):
        self.retries = retries
        self.bind = bind
        self.queue_url = queue_url or DEFAULT_QUEUE_URL

    def __call__(self, func):
        self.func = func
        return self

    def apply_async(
        self, args=[], kwargs={}, queue_url=None, countdown=default_delay
    ):
        body = {
            "_func_module": self.func.__module__,
            "_func_name": self.func.__name__,
            "args": args,
            "kwargs": kwargs,
            "retries": self.retries,
        }
        
        queue_url = queue_url or self.queue_url
        try:
            response = sqs_client.send_message(
                QueueUrl=queue_url, DelaySeconds=countdown, MessageBody=json.dumps(body)
            )
        except ClientError as err:
            data_exception = {
                "err": str(err),
                "body": str(body),
                "queue_url": queue_url,
                "aws_access_key_id": AWS_ACCESS_KEY_ID,
            }
            sentry_sdk.capture_message(str(data_exception))
        finally:
            return response["MessageId"]

    def apply(self, args=[], kwargs={}):
        return self._run(0, *args, **kwargs)

    def _save_request(self, *args, **kwargs):
        self.request_args = [*args]
        self.request_kwargs = kwargs

    def _run(self, retries, *args, **kwargs):
        self.retries = retries
        self._save_request(*args, **kwargs)

        if self.bind:
            return self.func(self, *args, **kwargs)
        return self.func(*args, **kwargs)

    def retry(
        self,
        err,
        max_retries=DEFAULT_MAX_RETRIES,
        countdown=DEFAULT_RETRY_DELAY,
        queue_url=None,
    ):
        self.retries += 1

        if self.retries >= max_retries:
            raise SQSTaskMaxRetriesExceededError(
                f"Task achieve the max retries possible: {max_retries}"
            )
        
        queue_url = queue_url or self.queue_url
        self.apply_async(
            args=self.request_args,
            kwargs=self.request_kwargs,
            queue_url=queue_url,
            countdown=countdown,
        )
        sentry_sdk.capture_message(str(err))
        return


class SQSHandler:
    def __init__(self, body):
        self.body = json.loads(body)

    def apply(self):
        module = importlib.import_module(self.body["_func_module"])
        sqs_task = getattr(module, self.body["_func_name"])

        return sqs_task._run(
            self.body["retries"], *self.body["args"], **self.body["kwargs"]
        )

    def sqs_delete_message(self, queue_url, receipt_handle):
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
