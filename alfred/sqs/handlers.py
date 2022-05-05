import importlib
import json

from . import sqs_client


class BaseHandler:
    def __init__(self, body):
        self.body = json.loads(body)

    def apply(self):
        module = importlib.import_module(self.body["_func_module"])
        sqs_task = getattr(module, self.body["_func_name"])

        return sqs_task._run(
            self.body["retries"], *self.body["args"], **self.body["kwargs"]
        )


class SQSHandler(BaseHandler):
    def sqs_delete_message(self, queue_url, receipt_handle):
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)


class DeadTaskHandler(BaseHandler):
    pass
