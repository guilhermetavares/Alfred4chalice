import base64

import pytest

from alfred.auth import BasicAuthUser


@pytest.fixture(scope="function")
def basic_auth_user():
    BasicAuthUser(username="admin", password="1234", routes=["my_fake_route"],).save()

    return BasicAuthUser.get("admin")


@pytest.fixture()
def basic_auth_token_valid(basic_auth_user):
    basic_auth = f"{basic_auth_user.username}:{basic_auth_user.password}"
    auth64 = base64.b64encode(bytes(basic_auth, "utf-8"))
    return f"Basic {auth64.decode('utf-8')}"


@pytest.fixture()
def basic_auth_token_invalid():
    basic_auth = "fake_user:fake_password"
    auth64 = base64.b64encode(bytes(basic_auth, "utf-8"))
    return f"Basic {auth64.decode('utf-8')}"
