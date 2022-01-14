import re

import phonenumbers


def only_digits(value: str):
    return "".join(filter(lambda i: i.isdigit(), value))


def has_accent(value):
    reg = "[\u00C0-\u00FF]"
    return bool(re.search(reg, value))


def is_email_valid(value):
    reg = r"^([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)$"  # noqa: E501
    return bool(re.match(reg, value))


def is_br_phone_valid(value):
    phone = f"+55{only_digits(value)}"
    phone_parsed = phonenumbers.parse(phone, "BR")
    return phonenumbers.is_valid_number(phone_parsed)
