from datetime import datetime

from creditcard import CreditCard
from dateutil.relativedelta import relativedelta
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
    ):
        super().__init__()
        self.error_messages["not_numeric_error_msg"] = not_numeric_error_msg
        self.error_messages["size_error_msg"] = size_error_msg


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
    ):
        super().__init__()
        self.error_messages["format_error_msg"] = format_error_msg
        self.error_messages["expired_error_msg"] = expired_error_msg


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


class CardNumberField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        cc = CreditCard(value)
        if not cc.is_valid():
            raise ValidationError(self.error_messages["card_error"])
        return cc.number

    def __init__(self, card_error_msg="Cartão inválido"):
        super().__init__()
        self.error_messages["card_error"] = card_error_msg
