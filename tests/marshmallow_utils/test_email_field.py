import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields import EmailField


def test_email_is_subclass():
    assert issubclass(EmailField, fields.String)


def test_email_invalid_has_accent_default_message():
    field = EmailField()
    email = "esquilão@gmail.com"

    with pytest.raises(ValidationError) as err:
        field._deserialize(email, "email", {"email": email})

    assert err.value.args[0] == "Não é permitido acentuação"


def test_email_invalid_has_accent_custom_message():
    accent_error_msg = "Some error message"
    field = EmailField(accent_error_msg=accent_error_msg)
    email = "esquilão@gmail.com"

    with pytest.raises(ValidationError) as err:
        field._deserialize(email, "email", {"email": email})

    assert err.value.args[0] == accent_error_msg


@pytest.mark.parametrize("email", ["foobar.com", "foo@bar", "@@bar.com"])
def test_email_invalid_default_message(email):
    field = EmailField()

    with pytest.raises(ValidationError) as err:
        field._deserialize(email, "email", {"email": email})

    assert err.value.args[0] == "Formato de e-mail inválido"


def test_email_invalid_custom_message():
    email_error_msg = "Some error message"
    field = EmailField(email_error_msg=email_error_msg)
    email = "foo@bar"

    with pytest.raises(ValidationError) as err:
        field._deserialize(email, "email", {"email": email})

    assert err.value.args[0] == email_error_msg


def test_email_valid():
    field = EmailField()
    email = "foo@bar.com"

    value = field._deserialize(email, "email", {"email": email})

    assert value == email
