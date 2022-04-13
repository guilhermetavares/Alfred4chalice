from chalice import AuthResponse

from .exceptions import NotAuthorized
from .models import BasicAuthUser
from .utils import get_credentials


def basic_auth_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    if not username and not password:
        raise NotAuthorized(401, "Não autorizado")

    routes = BasicAuthUser.login(username, password)

    return AuthResponse(routes=routes, principal_id=username)
