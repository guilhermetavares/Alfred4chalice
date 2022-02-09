import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.card_holder import CardHolderField


def test_cardholder_is_subclass():
    assert issubclass(CardHolderField, fields.String)


def test_cardholder_invalid_size_default_message():
    field = CardHolderField()
    card_holder = "Ana"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_holder, "holder", {"holder": card_holder})

    assert err.value.args[0] == "O titular deve conter mais do que 4 dígitos"


def test_cardholder_invalid_size_custom_message():
    invalid_size = "Some error message"
    field = CardHolderField(size_error_msg=invalid_size)
    card_holder = "Ana"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_holder, "holder", {"holder": card_holder})

    assert err.value.args[0] == invalid_size


def test_cardholder_valid():
    field = CardHolderField()
    card_holder = "Esquilo"

    value = field._deserialize(card_holder, "holder", {"holder": card_holder})

    assert value == card_holder
