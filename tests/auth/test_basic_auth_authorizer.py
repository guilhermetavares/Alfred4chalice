import pytest
from chalice.app import AuthRequest

from alfred.auth.basic_auth_authorizer import basic_auth_authorizer
from alfred.auth.exceptions import NotAuthorized


def test_basic_auth_authorizer_authorized(basic_auth_token_valid, basic_auth_user):
    auth_request = AuthRequest(
        auth_type="GET", token=basic_auth_token_valid, method_arn=""
    )

    auth_response = basic_auth_authorizer(auth_request=auth_request)

    assert auth_response.routes == basic_auth_user.routes
    assert auth_response.principal_id == basic_auth_user.username


def test_basic_auth_authorizer_unauthorized(
    basic_auth_token_invalid,
):
    auth_request = AuthRequest(
        auth_type="GET", token=basic_auth_token_invalid, method_arn=""
    )

    auth_response = basic_auth_authorizer(auth_request=auth_request)
    assert auth_response.routes == []
    assert auth_response.principal_id == "fake_user"


def test_basic_auth_authorizer_not_authorized_error():
    token = "b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIxYmRhZ"
    "mZjLWU1OTAtNGUyYy05ZjQxLTBlMzJmODAyYWVjNSIsInRva2VuIjpudWxsLCJleH"
    "AiOjE2NDk5Mzc5MDJ9.ByytFVSuR8y8cWkZMJMl8R6gsXfSS57Hh8mHJYFVvl0'"

    auth_request = AuthRequest(auth_type="GET", token=token, method_arn="")

    with pytest.raises(NotAuthorized):
        basic_auth_authorizer(auth_request=auth_request)
