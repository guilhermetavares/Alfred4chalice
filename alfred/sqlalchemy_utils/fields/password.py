import hashlib
import os

from sqlalchemy import types

ALFRED_PASSWORD_SALT = os.environ.get("ALFRED_PASSWORD_SALT", "esquilo")


def hash_password(raw_password):
    value_encode = raw_password.encode()

    password = hashlib.pbkdf2_hmac(
        "sha512", value_encode, ALFRED_PASSWORD_SALT.encode(), 100000
    ).hex()
    return password


class PasswordType(types.TypeDecorator):
    impl = types.VARBINARY(128)

    def process_bind_param(self, value, dialect):
        try:
            password = hash_password(value)
        except AttributeError:
            return None

        return password.encode()

    def process_result_value(self, value, dialect):
        try:
            return value.decode()
        except AttributeError:
            return None
