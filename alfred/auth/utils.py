import base64
from datetime import datetime, timedelta

import jwt
from cryptography.fernet import Fernet

from alfred.settings import (
    FERNET_CRYPT_KEY,
    JWT_ALGORITHM,
    JWT_CONTEXT_ARGS,
    JWT_EXP_DELTA_SECONDS,
    JWT_SECRET,
)


def get_credentials(auth64):
    decoded = base64.b64decode(auth64).decode("utf-8")
    username, password = decoded.split(":")
    return username, password


class JWTException(Exception):
    pass


def _validate_settings():
    if not all([JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, JWT_SECRET, FERNET_CRYPT_KEY]):
        raise JWTException({"error": "Missing JWT settings."})


def encode_auth(id, date=None, device_id=None, token=None, verify_code=None):
    _validate_settings()

    func_args = locals()

    if date is None:
        date = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)

    payload = {"id": str(id), "exp": date}

    f = Fernet(FERNET_CRYPT_KEY)

    for context_arg in JWT_CONTEXT_ARGS:
        if func_args.get(context_arg):
            payload[context_arg] = f.encrypt(func_args[context_arg].encode()).decode()

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_auth(token):
    _validate_settings()

    payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    f = Fernet(FERNET_CRYPT_KEY)

    for context in JWT_CONTEXT_ARGS:
        if payload.get(context):
            payload[context] = f.decrypt(payload[context].encode()).decode()

    return payload
