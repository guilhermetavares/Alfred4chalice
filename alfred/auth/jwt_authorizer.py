import jwt
from chalice import AuthResponse

from .utils import decode_auth


def jwt_authorizer(auth_request, encrypted_fields=[]):
    token = auth_request.token.replace("Token ", "")
    try:
        payload = decode_auth(token, encrypted_fields)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return AuthResponse(routes=[], principal_id="")

    principal_id = payload.pop("id")

    return AuthResponse(routes=["*"], principal_id=principal_id, context=payload,)
