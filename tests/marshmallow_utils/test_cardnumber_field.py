import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields import CardNumberField


def test_cardnumber_is_subclass():
    assert issubclass(CardNumberField, fields.String)


def test_cardnumber_invalid_default_message():
    field = CardNumberField()
    card_number = "123"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_number, "number", {"number": card_number})

    assert err.value.args[0] == "Cartão inválido"


def test_cardnumber_invalid_custom_message():
    card_err_msg = "Some error message"
    field = CardNumberField(card_error_msg=card_err_msg)
    card_number = "123"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_number, "number", {"number": card_number})

    assert err.value.args[0] == card_err_msg


def test_cardnumber_valid_without_mask():
    field = CardNumberField()
    card_number = "5299447679402836"

    value = field._deserialize(card_number, "number", {"number": card_number})

    assert value == "5299447679402836"


@pytest.mark.parametrize(
    "masked_document, document",
    [
        ("5299.4476.7940.2836", "5299447679402836"),
        ("5299 4476 7940 2836", "5299447679402836"),
        ("5299-4476-7940-2836", "5299447679402836"),
        ("52994476.79402836", "5299447679402836"),
    ],
)
def test_cardnumber_valid_with_mask(masked_document, document):
    field = CardNumberField()

    value = field._deserialize(masked_document, "number", {"number": masked_document})

    assert value == document
