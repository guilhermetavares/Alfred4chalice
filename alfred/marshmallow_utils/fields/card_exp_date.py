from datetime import datetime

from dateutil.relativedelta import relativedelta
from marshmallow import ValidationError, fields


class CardExpDateField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        try:
            exp_date = datetime.strptime(value, "%m/%Y")
        except ValueError:
            raise ValidationError(self.error_messages["error_msg"])

        if (exp_date + relativedelta(day=31)) < datetime.today():
            raise ValidationError(self.error_messages["error_msg"])

        return value

    def __init__(self, error_msg="Insira uma data válida", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["error_msg"] = error_msg
