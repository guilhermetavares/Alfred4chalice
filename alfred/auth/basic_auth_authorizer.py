from chalice import AuthResponse

from .models import BasicAuthUser
from .utils import get_credentials


def basic_auth_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    routes = BasicAuthUser.login(username, password)

    return AuthResponse(routes=routes, principal_id=username)
