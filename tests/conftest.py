import pytest
from botocore.stub import Stubber

from alfred.aws.s3 import s3_client
from alfred.dynamodb_create_tables import dynamodb_create_tables
from alfred.sqs.sqs import sqs_client


def pytest_configure(config):
    dynamodb_create_tables()


@pytest.fixture(autouse=True)
def sqs_stub():
    with Stubber(sqs_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(autouse=True)
def s3_stub():
    with Stubber(s3_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_query_parameters": [("secret", "ANY_SECRET")],
    }
