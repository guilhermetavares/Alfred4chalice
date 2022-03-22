from pynamodb.models import Model
from alfred.settings import DYNAMODB_HOST, DYNAMODB_PREFIX
from pynamodb.attributes import UnicodeAttribute, JSONAttribute, ListAttribute, NumberAttribute
from pynamodb.exceptions import DoesNotExist, GetError
from uuid import uuid4


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
