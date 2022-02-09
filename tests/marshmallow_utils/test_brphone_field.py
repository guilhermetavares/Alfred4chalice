import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.br_phone import BRPhoneField


def test_brphone_is_subclass():
    assert issubclass(BRPhoneField, fields.String)


def test_brphone_invalid_size_default_message():
    field = BRPhoneField()
    phone = "1234"

    with pytest.raises(ValidationError) as err:
        field._deserialize(phone, "phone", {"phone": phone})

    assert err.value.args[0] == "Número de telefone deve conter 11 dígitos"


def test_brphone_invalid_custom_size_custom_message():
    size_error_msg = "Some error message"
    field = BRPhoneField(size=5, size_error_msg=size_error_msg)
    phone = "123"

    with pytest.raises(ValidationError) as err:
        field._deserialize(phone, "phone", {"phone": phone})

    assert err.value.args[0] == size_error_msg


@pytest.mark.parametrize("phone", ["11111111111", "00999999999", "00123456789"])
def test_brphone_invalid_default_message(phone):
    field = BRPhoneField()

    with pytest.raises(ValidationError) as err:
        field._deserialize(phone, "phone", {"phone": phone})

    assert err.value.args[0] == "Telefone inválido"


def test_brphone_invalid_custom_message():
    phone_error_msg = "Some error message"
    field = BRPhoneField(phone_error_msg=phone_error_msg)
    phone = "11111111111"

    with pytest.raises(ValidationError) as err:
        field._deserialize(phone, "phone", {"phone": phone})

    assert err.value.args[0] == phone_error_msg


def test_brphone_valid_without_mask():
    field = BRPhoneField()
    phone = "16912345678"

    value = field._deserialize(phone, "phone", {"phone": phone})

    assert value == "16912345678"


@pytest.mark.parametrize(
    "masked_phone, phone",
    [
        ("(16) 9 1234-5678", "16912345678"),
        ("16 91234 5678", "16912345678"),
        ("16-912345678", "16912345678"),
        ("16. 9123.45678", "16912345678"),
    ],
)
def test_brphone_valid_with_mask(masked_phone, phone):
    field = BRPhoneField()

    value = field._deserialize(masked_phone, "phone", {"phone": masked_phone})

    assert value == phone
