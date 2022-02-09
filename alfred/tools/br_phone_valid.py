import phonenumbers

from .core import only_digits


def is_br_phone_valid(value):
    phone = f"+55{only_digits(value)}"
    phone_parsed = phonenumbers.parse(phone, "BR")
    return phonenumbers.is_valid_number(phone_parsed)
