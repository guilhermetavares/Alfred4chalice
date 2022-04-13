from chalice import AuthResponse

from alfred.cache.walrus_cache import Cache

from .exceptions import NotAuthorized
from .models import BasicAuthUser
from .utils import get_credentials


def basic_auth_cached_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    if not username and not password:
        raise NotAuthorized(401, "Não autorizado")

    CACHE_KEY = f"alfred_basic_auth_{username}"
    data = Cache.get(CACHE_KEY, None)

    if data and password == data["password"]:
        return AuthResponse(routes=data["routes"], principal_id=data["username"])

    routes = BasicAuthUser.login(username, password)

    cached_auth = {"username": username, "password": password, "routes": routes}
    cache_time = 60 * 60
    Cache.set(CACHE_KEY, cached_auth, cache_time)

    return AuthResponse(routes=routes, principal_id=username)
