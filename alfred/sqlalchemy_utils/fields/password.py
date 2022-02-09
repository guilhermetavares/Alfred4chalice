from sqlalchemy import types

from .utils import hash_password


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
