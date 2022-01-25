from datetime import datetime
from unittest.mock import patch

import pytest
from chalice.app import AuthRequest
from freezegun import freeze_time
from jwt import DecodeError, ExpiredSignatureError

from alfred.auth import JWTException, decode_auth, encode_auth, jwt_authorizer


@pytest.mark.parametrize(
    "key, value",
    [("any", "arg"), ("token", "fake_token"), ("verify_code", "1234"), ("foo", "bar")],
)
@freeze_time("2021-01-01")
def test_jwt_authorizer_authorized_with_kwargs(key, value):

    kwargs = {key: value}
    token = encode_auth(id="fake_id", **kwargs)

    auth_request = AuthRequest(auth_type="GET", token=token, method_arn="")

    auth_response = jwt_authorizer(auth_request=auth_request)

    assert auth_response.routes == ["*"]
    assert auth_response.principal_id == "fake_id"
    assert auth_response.context[key] == value


@patch("alfred.auth.authorizers.decode_auth")
def test_jwt_authorizer_expired_error(mock_decode):
    mock_decode.side_effect = ExpiredSignatureError("fake_error")

    token = encode_auth(id="fake_id")
    auth_request = AuthRequest(auth_type="GET", token=token, method_arn="")

    auth_response = jwt_authorizer(auth_request=auth_request)
    assert auth_response.routes == []
    assert auth_response.principal_id == ""
    assert auth_response.context == {}


@patch("alfred.auth.authorizers.decode_auth")
def test_jwt_authorizer_decode_rror(mock_decode):
    mock_decode.side_effect = DecodeError("fake_error")

    token = encode_auth(id="fake_id")
    auth_request = AuthRequest(auth_type="GET", token=token, method_arn="")

    auth_response = jwt_authorizer(auth_request=auth_request)
    assert auth_response.routes == []
    assert auth_response.principal_id == ""
    assert auth_response.context == {}


@freeze_time("2021-01-01")
def test_jwt_encode_decode_with_date():
    fake_date = datetime(2021, 1, 1)

    token = encode_auth(id="fake_id", date=fake_date)
    assert token is not None

    fake_decode = decode_auth(token)
    assert fake_decode["id"] == "fake_id"
    assert fake_decode["exp"] is not None


@freeze_time("2021-01-01")
def test_jwt_encode_decode_without_date():
    token = encode_auth(id="fake_id")
    assert token is not None

    fake_decode = decode_auth(token)
    assert fake_decode["id"] == "fake_id"
    assert fake_decode["exp"] is not None


@patch("alfred.auth.utils.JWT_SECRET", None)
def test_jwt_decode_missing_settings():
    with pytest.raises(JWTException) as err:
        decode_auth("abcd")

    assert err.value.args[0] == {"error": "Missing JWT settings."}


@patch("alfred.auth.utils.JWT_SECRET", None)
def test_jwt_encode_missing_settings():
    with pytest.raises(JWTException) as err:
        encode_auth(id="fake_id")

    assert err.value.args[0] == {"error": "Missing JWT settings."}
