from marshmallow import ValidationError, fields

from alfred.tools import has_accent, is_br_phone_valid, is_email_valid, only_digits


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


class BRPhoneField(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        phone = only_digits(value)
        if len(phone) != self.size:
            raise ValidationError(self.error_messages["size_error_msg"])
        if not is_br_phone_valid(value):
            raise ValidationError(self.error_messages["phone_error_msg"])
        return phone

    def __init__(
        self,
        size=11,
        size_error_msg="Número de telefone deve conter 11 dígitos",
        phone_error_msg="Telefone inválido",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.size = size
        self.error_messages["size_error_msg"] = size_error_msg
        self.error_messages["phone_error_msg"] = phone_error_msg
