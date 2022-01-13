from marshmallow import ValidationError, fields


class CardHolderField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if len(value) <= 4:
            raise ValidationError(self.error_messages["size_error_msg"])

        return value

    def __init__(
        self, size_error_msg="O titular deve conter mais do que 4 dígitos",
    ):
        super().__init__()
        self.error_messages["size_error_msg"] = size_error_msg
