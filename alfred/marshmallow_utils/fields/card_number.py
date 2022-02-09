from creditcard import CreditCard
from marshmallow import ValidationError, fields


class CardNumberField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        cc = CreditCard(value)
        if not cc.is_valid():
            raise ValidationError(self.error_messages["card_error"])
        return cc.number

    def __init__(self, card_error_msg="Cartão inválido", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["card_error"] = card_error_msg
