from datetime import datetime

from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError, fields


class CardExpDateField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        try:
            exp_date = datetime.strptime(value, "%m/%Y")
        except ValueError:
            raise ValidationError(self.error_messages["format_error_msg"])

        if (exp_date + relativedelta(day=31)) < datetime.today():
            raise ValidationError(self.error_messages["expired_error_msg"])

        return value

    def __init__(
        self,
        format_error_msg="O formato da data de expiração deve ser mm/YYYY",
        expired_error_msg="Cartão expirado",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_messages["format_error_msg"] = format_error_msg
        self.error_messages["expired_error_msg"] = expired_error_msg
