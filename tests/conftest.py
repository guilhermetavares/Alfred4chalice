from alfred.dynamodb_create_tables import dynamodb_create_tables


def pytest_configure(config):
    dynamodb_create_tables()
