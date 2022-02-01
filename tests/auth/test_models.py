from datetime import datetime

from freezegun import freeze_time
from pynamodb.models import Model

from alfred.auth.models import BasicAuthUser
from alfred.settings import DYNAMODB_PREFIX


def test_user_is_instance():
    assert issubclass(BasicAuthUser, Model)


def test_user_tablename():
    assert BasicAuthUser.Meta.table_name == f"{DYNAMODB_PREFIX}_basicauth_user"


@freeze_time("2021-01-01 00:00:01")
def test_user_to_json():
    user = BasicAuthUser(
        username="Esquilo",
        password="1234",
        routes=["/v1/foo"],
        created_at=datetime.utcnow(),
        metadata={"foo": "bar"},
    )

    expected_json = {
        "username": "Esquilo",
        "routes": ["/v1/foo"],
        "created_at": "2021-01-01 00:00:01",
        "metadata": {"foo": "bar"},
    }

    assert user.to_json == expected_json


@freeze_time("2021-01-01 00:00:01")
def test_user_to_json_without_metadata():
    user = BasicAuthUser(
        username="Esquilo",
        password="1234",
        routes=["/v1/foo"],
        created_at=datetime.utcnow(),
    )

    expected_json = {
        "username": "Esquilo",
        "routes": ["/v1/foo"],
        "created_at": "2021-01-01 00:00:01",
        "metadata": None,
    }

    assert user.to_json == expected_json


def test_user_login_success(basic_auth_user):
    password = basic_auth_user.password
    username = basic_auth_user.username
    assert BasicAuthUser.login(username, password) == basic_auth_user.routes


def test_user_login_wrong_password(basic_auth_user):
    username = basic_auth_user.username
    assert BasicAuthUser.login(username, "wrong_pass") == []


def test_user_login_empty_username(basic_auth_user):
    assert BasicAuthUser.login(None, "wrong_pass") == []


def test_user_login_empty_password(basic_auth_user):
    username = basic_auth_user.username
    assert BasicAuthUser.login(username, None) == []


def test_user_login_does_not_exist():
    assert BasicAuthUser.login("fakeuser", "wrong_pass") == []
