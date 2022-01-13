import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields import CardExpDateField


def test_cardexpdate_is_subclass():
    assert issubclass(CardExpDateField, fields.String)


def test_cardexpdate_invalid_format_default_message():
    field = CardExpDateField()
    exp_date = "wrong"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == "O formato da data de expiração deve ser mm/YYYY"


def test_cardexpdate_invalid_format_custom_message():
    format_error_msg = "Some error message"
    field = CardExpDateField(format_error_msg=format_error_msg)
    exp_date = "wrong"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == format_error_msg


def test_cardexpdate_invalid_expired_default_message():
    field = CardExpDateField()
    exp_date = "01/2001"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == "Cartão expirado"


def test_cardexpdate_invalid_expired_custom_message():
    format_error_msg = "Some error message"
    field = CardExpDateField(expired_error_msg=format_error_msg)
    exp_date = "01/2001"

    with pytest.raises(ValidationError) as err:
        field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert err.value.args[0] == format_error_msg


def test_cardexpdate_valid():
    field = CardExpDateField()
    exp_date = "01/2100"

    value = field._deserialize(exp_date, "exp_date", {"exp_date": exp_date})

    assert value == exp_date
