import base64
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


def encode_auth(id, token=None, date=None):
    _validate_settings()

    if date is None:
        date = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)

    if token:
        f = Fernet(FERNET_CRYPT_KEY)
        token = f.encrypt(token.encode()).decode()

    payload = {"id": str(id), "token": token, "exp": date}
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_auth(token):
    _validate_settings()

    payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    if payload.get("token"):
        f = Fernet(FERNET_CRYPT_KEY)
        payload["token"] = f.decrypt(payload["token"].encode()).decode()
    return payload
