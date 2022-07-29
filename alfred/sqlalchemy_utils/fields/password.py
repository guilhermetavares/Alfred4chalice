from sqlalchemy import types

from .utils import hash_password


class PasswordType(types.TypeDecorator):
    impl = types.Unicode(128)

    def process_bind_param(self, value, dialect):
        try:
            password = hash_password(value)
        except AttributeError:
            return None

        return password
