from marshmallow import ValidationError, fields
from tools.br_state_valid import is_br_state_valid


class BRStateField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if not is_br_state_valid(value):
            raise ValidationError(self.error_messages["state_error_msg"])

        return value

    def __init__(self, state_error_msg="Estado inválido", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["state_error_msg"] = state_error_msg
