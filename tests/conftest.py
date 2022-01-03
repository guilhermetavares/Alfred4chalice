import pytest
from botocore.stub import Stubber

from alfred.dynamodb_create_tables import dynamodb_create_tables
from alfred.sqs.sqs import sqs_client


def pytest_configure(config):
    dynamodb_create_tables()


@pytest.fixture(autouse=True)
def sqs_stub():
    with Stubber(sqs_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
