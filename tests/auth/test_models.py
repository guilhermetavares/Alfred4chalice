from datetime import datetime

import pytest
from freezegun import freeze_time
from pynamodb.models import Model

from alfred.auth.exceptions import InvalidMetadataException, InvalidRoutesException
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


def test_user_add_routes_success(basic_auth_user):
    new_routes = ["foo", "bar"]
    basic_auth_user.add_routes(new_routes)

    assert new_routes[0] in basic_auth_user.routes
    assert new_routes[1] in basic_auth_user.routes


def test_user_add_routes_empty(basic_auth_user):
    new_routes = []
    with pytest.raises(InvalidRoutesException) as err:
        basic_auth_user.add_routes(new_routes)

    assert err.value.args[0] == "New routes must be a valid list of routes"


def test_user_add_routes_invalid_routes(basic_auth_user):
    new_routes = {}
    with pytest.raises(InvalidRoutesException) as err:
        basic_auth_user.add_routes(new_routes)

    assert err.value.args[0] == "New routes must be a valid list of routes"


def test_user_empty_metadata_add_metadata_success(basic_auth_user):
    assert basic_auth_user.metadata is None

    new_metadata = {"foo": "bar"}
    basic_auth_user.add_metadata(new_metadata)

    assert basic_auth_user.metadata["foo"] == "bar"


def test_user_has_metadata_add_metadata_success(basic_auth_user):
    basic_auth_user.metadata = {"key": "value"}
    assert basic_auth_user.metadata is not None

    new_metadata = {"foo": "bar"}
    basic_auth_user.add_metadata(new_metadata)

    assert basic_auth_user.metadata["foo"] == "bar"


def test_user_add_metadata_invalid_metadata(basic_auth_user):
    new_metadata = []
    with pytest.raises(InvalidMetadataException) as err:
        basic_auth_user.add_metadata(new_metadata)

    assert err.value.args[0] == "New metadata must be a valid dictionary"
