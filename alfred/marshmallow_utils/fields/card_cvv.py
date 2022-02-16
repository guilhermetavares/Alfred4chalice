from marshmallow import ValidationError, fields


class CardCvvField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if not value.isnumeric():
            raise ValidationError(self.error_messages["not_numeric_error_msg"])
        if len(value) not in [3, 4]:
            raise ValidationError(self.error_messages["size_error_msg"])
        return value

    def __init__(
        self,
        not_numeric_error_msg="Apenas números são aceitos",
        size_error_msg="O CVV deve conter 3 ou 4 números",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_messages["not_numeric_error_msg"] = not_numeric_error_msg
        self.error_messages["size_error_msg"] = size_error_msg
