import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields import CardCvvField


def test_cardcvv_is_subclass():
    assert issubclass(CardCvvField, fields.String)


def test_cardcvv_invalid_not_numeric_default_message():
    field = CardCvvField()
    card_cvv = "12a"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_cvv, "cvv", {"cvv": card_cvv})

    assert err.value.args[0] == "Apenas números são aceitos"


def test_cardcvv_invalid_not_numeric_custom_message():
    not_numeric_error_msg = "Some error message"
    field = CardCvvField(not_numeric_error_msg=not_numeric_error_msg)
    card_cvv = "12a"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_cvv, "cvv", {"cvv": card_cvv})

    assert err.value.args[0] == not_numeric_error_msg


def test_cardcvv_invalid_size_default_message():
    field = CardCvvField()
    card_cvv = "12"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_cvv, "cvv", {"cvv": card_cvv})

    assert err.value.args[0] == "O CVV deve conter 3 ou 4 números"


def test_cardcvv_invalid_size_custom_message():
    not_numeric_error_msg = "Some error message"
    field = CardCvvField(size_error_msg=not_numeric_error_msg)
    card_cvv = "12"

    with pytest.raises(ValidationError) as err:
        field._deserialize(card_cvv, "cvv", {"cvv": card_cvv})

    assert err.value.args[0] == not_numeric_error_msg


def test_cardcvv_valid():
    field = CardCvvField()
    card_cvv = "123"

    value = field._deserialize(card_cvv, "cvv", {"cvv": card_cvv})

    assert value == card_cvv
