import base64

from chalice import AuthResponse

from .models import BasicAuthUser


def get_credentials(auth64):
    decoded = base64.b64decode(auth64).decode("utf-8")
    username, password = decoded.split(":")
    return username, password


def basic_auth_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    routes = BasicAuthUser.login(username, password)

    return AuthResponse(routes=routes, principal_id=username)
