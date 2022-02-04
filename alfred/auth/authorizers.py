import jwt
from chalice import AuthResponse

from .models import BasicAuthUser
from .utils import decode_auth, get_credentials
from alfred.cache.walrus_cache import Cache

def basic_auth_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    routes = BasicAuthUser.login(username, password)

    return AuthResponse(routes=routes, principal_id=username)


def basic_auth_cached_authorizer(auth_request):
    auth64 = auth_request.token.replace("Basic ", "")
    username, password = get_credentials(auth64)

    CACHE_KEY = f"alfred_basic_auth_{username}"
    data = Cache.get(CACHE_KEY, None)

    if data and password == data["password"]:
        return AuthResponse(routes=data["routes"], principal_id=data["username"])

    routes = BasicAuthUser.login(username, password)

    cached_auth = {"username" : username, "password" : password, "routes" : routes}
    cache_time = 60*60
    Cache.set(CACHE_KEY, cached_auth, cache_time)

    return AuthResponse(routes=routes, principal_id=username)



def jwt_authorizer(auth_request, encrypted_fields=[]):
    token = auth_request.token.replace("Token ", "")
    try:
        payload = decode_auth(token, encrypted_fields)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return AuthResponse(routes=[], principal_id="")

    principal_id = payload.pop("id")

    return AuthResponse(routes=["*"], principal_id=principal_id, context=payload,)
