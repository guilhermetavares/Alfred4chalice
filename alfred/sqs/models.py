import logging
from uuid import uuid4

from pynamodb.attributes import (
    JSONAttribute,
    ListAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model

from alfred.settings import DYNAMODB_HOST, DYNAMODB_PREFIX
from alfred.sqs.handlers import DeadTaskHandler

logger = logging.getLogger("base")


class DeadTask(Model):
    class Meta:
        host = DYNAMODB_HOST
        table_name = f"{DYNAMODB_PREFIX}_dead_task"

    id = UnicodeAttribute(hash_key=True, default=str(uuid4))
    function_module = UnicodeAttribute()
    function_name = UnicodeAttribute()
    function_args = ListAttribute()
    function_kwargs = JSONAttribute()
    function_retries = NumberAttribute()
    queue_url = UnicodeAttribute()

    def run(self):
        body = {
            "_func_module": self.function_module,
            "_func_name": self.function_name,
            "args": self.function_args,
            "kwargs": self.function_kwargs,
            "retries": self.function_retries,
        }
        try:
            DeadTaskHandler(body).apply()
        except Exception as err:
            logger.error(
                {
                    "task_is_DeadTask": True,
                    "task_error_message": str(err),
                    "task_function_module": self.function_module,
                    "task_function_name": self.function_name,
                    "task_function_args": self.function_args,
                    "task_function_kwargs": self.function_kwargs,
                    "task_function_retries": self.function_retries,
                    "task_queue_url": self.queue_url,
                }
            )
        finally:
            self.delete()
