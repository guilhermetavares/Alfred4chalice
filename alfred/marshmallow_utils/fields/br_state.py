from marshmallow import ValidationError, fields
from tools.br_state_valid import is_br_state_valid


class BRStateField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):

        state = value.upper()

        if len(state) > 2:
            raise ValidationError(self.error_messages["format_error_msg"])

        if not is_br_state_valid(state):
            raise ValidationError(self.error_messages["state_error_msg"])

        return state

    def __init__(
        self,
        state_error_msg="Estado inválido",
        format_error_msg="Apenas siglas são aceitas",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_messages["format_error_msg"] = format_error_msg
        self.error_messages["state_error_msg"] = state_error_msg
