from alfred.sqlalchemy_utils.fields.password import (
    PasswordSaltType,
    hash_password,
    types,
)


def test_password_salt_type_impl():
    assert type(PasswordSaltType.impl) is types.VARBINARY
    assert PasswordSaltType.impl.length == 255


def test_password_salt_type_process_bind_param():
    pw = PasswordSaltType()
    password = pw.process_bind_param("1234", None)

    password_decode = password.decode()
    password_salt, password_hash = password_decode.split("-")

    assert len(password_salt) == 32
    assert len(password_hash) == 128

    assert hash_password("1234", password_salt) == password_hash


def test_password_salt_type_process_bind_param_with_value_as_none():
    pw = PasswordSaltType()
    password = pw.process_bind_param(None, None)
    assert password is None


def test_password_salt_type_process_result_value():
    pw = PasswordSaltType()
    password = pw.process_result_value(b"esquilo", None)
    assert password == "esquilo"


def test_password_salt_type_process_result_value_with_value_as_none():
    pw = PasswordSaltType()
    password = pw.process_result_value(None, None)
    assert password is None
