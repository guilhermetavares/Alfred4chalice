from alfred.sqlalchemy_utils.fields.password import PasswordType, types


def test_password_type_impl():
    assert type(PasswordType.impl) is types.VARBINARY
    assert PasswordType.impl.length == 128


def test_password_type_process_bind_param(hash_password_1234):
    pw = PasswordType()
    password = pw.process_bind_param("1234", None)
    assert password.decode() == hash_password_1234


def test_password_type_process_bind_param_with_value_as_none():
    pw = PasswordType()
    password = pw.process_bind_param(None, None)
    assert password is None


def test_password_type_process_result_value():
    pw = PasswordType()
    password = pw.process_result_value(b"esquilo", None)
    assert password == "esquilo"


def test_password_type_process_result_value_with_value_as_none():
    pw = PasswordType()
    password = pw.process_result_value(None, None)
    assert password is None
