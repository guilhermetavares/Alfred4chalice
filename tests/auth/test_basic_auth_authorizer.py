from chalice.app import AuthRequest

from alfred.auth import basic_auth_authorizer


def test_basic_auth_authorizer_authorized(basic_auth_token_valid, basic_auth_user):
    auth_request = AuthRequest(
        auth_type="GET", token=basic_auth_token_valid, method_arn=""
    )

    auth_response = basic_auth_authorizer(auth_request=auth_request)

    assert auth_response.routes == basic_auth_user.routes
    assert auth_response.principal_id == basic_auth_user.username


def test_basic_auth_authorizer_unauthorized(basic_auth_token_invalid,):
    auth_request = AuthRequest(
        auth_type="GET", token=basic_auth_token_invalid, method_arn=""
    )

    auth_response = basic_auth_authorizer(auth_request=auth_request)
    assert auth_response.routes == []
    assert auth_response.principal_id == "fake_user"
