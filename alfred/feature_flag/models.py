from pynamodb.attributes import JSONAttribute, UnicodeAttribute
from pynamodb.exceptions import DoesNotExist, GetError
from pynamodb.models import Model

from alfred.settings import DYNAMODB_HOST, DYNAMODB_PREFIX


class FeatureFlag(Model):
    class Meta:
        host = DYNAMODB_HOST
        table_name = f"{DYNAMODB_PREFIX}_feature_flag"

    id = UnicodeAttribute(hash_key=True)
    data = JSONAttribute()

    @classmethod
    def get_data(cls, id):
        try:
            return cls.get(id).data
        except (DoesNotExist, GetError):
            return None

    @classmethod
    def get_batch_feature_flag(cls, api_issues_keys):
        for flag in FeatureFlag.batch_get(api_issues_keys):
            return flag.data
