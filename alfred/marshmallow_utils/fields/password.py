from marshmallow import ValidationError, fields

from alfred.tools import only_digits


class PasswordNumberField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)

        if len(value) != len(only_digits(value)):
            raise ValidationError(self.error_messages["not_numeric_error_msg"])

        if len(only_digits(value)) != self.size:
            raise ValidationError(self.error_messages["size_error_msg"])

        return value

    def __init__(
        self,
        size=4,
        size_error_msg="A senha deve conter quatro números",
        not_numeric_error_msg="Apenas números são aceitos",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.size = size
        self.error_messages["size_error_msg"] = size_error_msg
        self.error_messages["not_numeric_error_msg"] = not_numeric_error_msg
