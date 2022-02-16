from pynamodb.models import Model
from alfred.settings import DYNAMODB_HOST, DYNAMODB_PREFIX
from pynamodb.attributes import UnicodeAttribute, JSONAttribute
from pynamodb.exceptions import DoesNotExist, GetError

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
        
