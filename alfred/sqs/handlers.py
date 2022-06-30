import importlib
import json

from . import sqs_client


class BaseHandler:
    def __init__(self, body):
        self.body = json.loads(body)

    def get_sqs_task(self):
        module = importlib.import_module(self.body["_func_module"])
        self.sqs_task = getattr(module, self.body["_func_name"])
        self.config_sqs_task()
        
    def config_sqs_task(self):
        pass  # pragma: no cover

    def apply(self):
        self.get_sqs_task()

        return self.sqs_task._run(
            self.body["retries"], *self.body["args"], **self.body["kwargs"]
        )


class SQSHandler(BaseHandler):
    def __init__(self, body, aws_request_id=None, message_id=None):
        super().__init__(body)
        self.aws_request_id = aws_request_id
        self.message_id = message_id
    
    def config_sqs_task(self):
        self.sqs_task.message_id = self.message_id
        self.sqs_task.aws_request_id = self.aws_request_id

    def sqs_delete_message(self, queue_url, receipt_handle):
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)


class DeadTaskHandler(BaseHandler):
    pass
