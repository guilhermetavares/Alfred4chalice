from alfred.auth.models import BasicAuthUser
from alfred.settings import DYNAMO_PREFIX


class DynamoDBException(Exception):
    pass


def dynamodb_create_tables():
    if not DYNAMO_PREFIX:
        raise DynamoDBException("DYNAMO_PREFIX environment variable must be set")

    if not BasicAuthUser.exists():
        BasicAuthUser.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


if __name__ == "__main__":
    dynamodb_create_tables()
