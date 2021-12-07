import hashlib
import uuid

from sqlalchemy import types

from alfred.settings import ALFRED_PASSWORD_SALT


def hash_password(raw_password, salt=None):
    value_encode = raw_password.encode()

    salt_encode = salt.encode() if salt else ALFRED_PASSWORD_SALT.encode()

    password = hashlib.pbkdf2_hmac("sha512", value_encode, salt_encode, 100000).hex()
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


class PasswordSaltType(types.TypeDecorator):
    impl = types.VARBINARY(255)

    def process_bind_param(self, value, dialect):
        try:
            salt = uuid.uuid4().hex
            password = hash_password(value, salt)
        except AttributeError:
            return None

        foo = f"{salt}-{password}"
        return foo.encode()

    def process_result_value(self, value, dialect):
        try:
            return value.decode()
        except AttributeError:
            return None
