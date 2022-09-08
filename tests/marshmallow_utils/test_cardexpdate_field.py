import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.card_exp_date import CardExpDateField


def test_cardexpdate_is_subclass():
    assert issubclass(CardExpDateField, fields.String)


def test_cardexpdate_invalid_format_default_message():
    field = CardExpDateField()
    exp_date = "wrong"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == "Insira uma data válida"


def test_cardexpdate_invalid_format_custom_message():
    error_msg = "Some error message"
    field = CardExpDateField(error_msg=error_msg)
    exp_date = "wrong"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == error_msg


def test_cardexpdate_invalid_expired_default_message():
    field = CardExpDateField()
    exp_date = "01/2001"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == "Insira uma data válida"


def test_cardexpdate_valid():
    field = CardExpDateField()
    exp_date = "01/2100"

    value = field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert value == exp_date
