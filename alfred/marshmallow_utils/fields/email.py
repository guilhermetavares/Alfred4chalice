from marshmallow import ValidationError, fields

from alfred.tools import has_accent, is_email_valid


class EmailField(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if has_accent(value):
            raise ValidationError(self.error_messages["accent_error_msg"])

        if not is_email_valid(value):
            raise ValidationError(self.error_messages["email_error_msg"])
        return value

    def __init__(
        self,
        accent_error_msg="Não é permitido acentuação",
        email_error_msg="Formato de e-mail inválido",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_messages["accent_error_msg"] = accent_error_msg
        self.error_messages["email_error_msg"] = email_error_msg
