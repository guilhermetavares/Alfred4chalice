import base64
import binascii
from datetime import datetime, timedelta

import jwt
from cryptography.fernet import Fernet

from alfred.settings import (
    FERNET_CRYPT_KEY,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_SECONDS,
    JWT_SECRET,
)

from .exceptions import JWTException


def get_credentials(auth64):
    try:
        decoded = base64.b64decode(auth64).decode("utf-8")
        username, password = decoded.split(":")
    except binascii.Error:
        username = None
        password = None

    return username, password


def _validate_settings():
    if not all([JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, JWT_SECRET, FERNET_CRYPT_KEY]):
        raise JWTException({"error": "Missing JWT settings."})


def _fernet_fields(encrypted_fields, method, **kwargs):

    conditions = [kwargs, encrypted_fields, method in ["encrypt", "decrypt"]]

    if not all(conditions):
        return kwargs

    payload = {}
    f = Fernet(FERNET_CRYPT_KEY)

    for field, value in kwargs.items():
        if field in encrypted_fields:
            action = f.__getattribute__(method)
            payload[field] = action(value.encode()).decode()
        else:
            payload[field] = value

    return payload


def encode_auth(id, date=None, encrypted_fields=[], **kwargs):
    _validate_settings()

    if date is None:
        date = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)

    base_payload = {"id": str(id), "exp": date, **kwargs}

    payload = _fernet_fields(
        encrypted_fields=encrypted_fields, method="encrypt", **base_payload
    )

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_auth(token, encrypted_fields=[]):
    _validate_settings()

    token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)

    payload = _fernet_fields(
        encrypted_fields=encrypted_fields, method="decrypt", **token
    )

    return payload
