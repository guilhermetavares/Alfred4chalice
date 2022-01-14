import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields import PasswordNumberField


def test_passwordnumber_is_subclass():
    assert issubclass(PasswordNumberField, fields.String)


def test_passwordnumber_invalid_not_numeric_default_message():
    field = PasswordNumberField()
    password = "abcd"

    with pytest.raises(ValidationError) as err:
        field._deserialize(password, "password", {"password": password})

    assert err.value.args[0] == "Apenas números são aceitos"


def test_passwordnumber_invalid_not_numeric_custom_message():
    not_numeric_error_msg = "Some error message"
    field = PasswordNumberField(not_numeric_error_msg=not_numeric_error_msg)
    password = "12a"

    with pytest.raises(ValidationError) as err:
        field._deserialize(password, "password", {"password": password})

    assert err.value.args[0] == not_numeric_error_msg


def test_passwordnumber_invalid_size_default_message():
    field = PasswordNumberField()
    password = "123"

    with pytest.raises(ValidationError) as err:
        field._deserialize(password, "password", {"password": password})

    assert err.value.args[0] == "A senha deve conter quatro números"


def test_passwordnumber_invalid_size_custom_message():
    size_error_msg = "Some error message"
    field = PasswordNumberField(size_error_msg=size_error_msg)
    password = "12"

    with pytest.raises(ValidationError) as err:
        field._deserialize(password, "password", {"password": password})

    assert err.value.args[0] == size_error_msg


def test_passwordnumber_valid():
    field = PasswordNumberField()
    password = "1234"

    value = field._deserialize(password, "password", {"password": password})

    assert value == password
