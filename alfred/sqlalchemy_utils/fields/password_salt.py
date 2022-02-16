import uuid
from random import randint

from sqlalchemy import types

from .utils import hash_password


class PasswordSaltType(types.TypeDecorator):
    impl = types.VARBINARY(255)

    def process_bind_param(self, value, dialect):
        try:
            salt = uuid.uuid4().hex
            interations = randint(90000, 99999)
            password = hash_password(value, salt, interations)
        except AttributeError:
            return None

        foo = f"{salt}-{interations}-{password}"
        return foo.encode()

    def process_result_value(self, value, dialect):
        try:
            return value.decode()
        except AttributeError:
            return None
