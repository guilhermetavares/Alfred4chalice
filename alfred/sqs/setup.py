import logging

from alfred.settings import SQS_QUEUE_URL
from alfred.sqs.handlers import SQSHandler

logger = logging.getLogger("base")


def handle_sqs_message(event, queue_url=None):
    queue_url = queue_url or SQS_QUEUE_URL
    for record in event:
        record_dict = record.to_dict()

        aws_request_id = record.context.aws_request_id
        body = record_dict["body"]
        message_id = record_dict["messageId"]

        handler = SQSHandler(body, aws_request_id, message_id)
        
        try:
            response = handler.apply()
        except Exception as err:
            logger.debug(
                {
                    "sqs_message_id": message_id,
                    "aws_request_id": aws_request_id,
                    "task_has_succeeded": False,
                    "task_error_message": str(err),
                    "task_function_module": handler.body["_func_module"],
                    "task_function_name": handler.body["_func_name"],
                    "task_function_args": handler.body["args"],
                    "task_function_kwargs": handler.body["kwargs"],
                    "task_function_retries": handler.body["retries"],
                    "task_response": None,
                }
            )
            raise err
        else:
            logger.debug(
                {
                    "sqs_message_id": message_id,
                    "aws_request_id": aws_request_id,
                    "task_has_succeeded": True,
                    "task_error_message": None,
                    "task_function_module": handler.body["_func_module"],
                    "task_function_name": handler.body["_func_name"],
                    "task_function_args": handler.body["args"],
                    "task_function_kwargs": handler.body["kwargs"],
                    "task_function_retries": handler.body["retries"],
                    "task_response": response,
                }
            )
        finally:
            handler.sqs_delete_message(queue_url, record.receipt_handle)
