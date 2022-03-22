from alfred.auth.models import BasicAuthUser
from alfred.feature_flag.models import FeatureFlag
from alfred.settings import DYNAMODB_PREFIX
from alfred.sqs.models import DeadTask


class DynamoDBException(Exception):
    pass


def dynamodb_create_tables():
    if not DYNAMODB_PREFIX:
        raise DynamoDBException("DYNAMODB_PREFIX environment variable must be set")

    if not BasicAuthUser.exists():
        BasicAuthUser.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
        
    if not FeatureFlag.exists():
        FeatureFlag.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

    if not DeadTask.exists():
        DeadTask.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

if __name__ == "__main__":
    dynamodb_create_tables()
