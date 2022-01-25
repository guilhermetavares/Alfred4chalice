import base64
from copy import deepcopy
from datetime import datetime, timedelta

import jwt
from cryptography.fernet import Fernet

from alfred.settings import (
    FERNET_CRYPT_KEY,
    JWT_ALGORITHM,
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


def encode_auth(id, date=None, **kwargs):
    _validate_settings()

    if date is None:
        date = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)

    payload = {"id": str(id), "exp": date}

    extra_args = kwargs
    if extra_args:
        f = Fernet(FERNET_CRYPT_KEY)
        for arg in extra_args:
            payload[arg] = f.encrypt(extra_args[arg].encode()).decode()

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_auth(token):
    _validate_settings()

    payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    f = Fernet(FERNET_CRYPT_KEY)

    extra_args = deepcopy(payload)
    extra_args.pop("id")
    extra_args.pop("exp")

    for key, value in extra_args.items():
        payload[key] = f.decrypt(value.encode()).decode()

    return payload
