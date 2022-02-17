import logging

from alfred.settings import SQS_QUEUE_URL
from alfred.sqs.sqs import SQSHandler

logger = logging.getLogger("base")


def handle_sqs_message(event, queue_url=None):
    queue_url = queue_url or SQS_QUEUE_URL
    for record in event:
        handler = SQSHandler(body=record.body)
        try:
            response = handler.apply()
        except Exception as err:
            logger.debug(
                {
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
