import uuid
from random import randint

from sqlalchemy import types

from .utils import hash_password


class PasswordSaltType(types.TypeDecorator):
    impl = types.Unicode(255)

    def process_bind_param(self, value, dialect):
        try:
            salt = uuid.uuid4().hex
            iterations = randint(90000, 99999)
            password = hash_password(value, salt, iterations)
        except AttributeError:
            return None

        return f"{salt}-{iterations}-{password}"
