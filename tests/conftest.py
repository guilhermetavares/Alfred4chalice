import pytest

from alfred.dynamodb_create_table import dynamodb_create_tables


def pytest_configure(config):
    dynamodb_create_tables()


@pytest.fixture(scope="module")
def hash_password_1234():
    return "201f5fd49dfdd09076a1dbb9651d9c592d64e999f3d1f09ffb099542e127cf7ed0a1cdee577648cf0f1ae34d1027e8eec33fea36b179cf655600175ca4d6d877"  # noqa E501
