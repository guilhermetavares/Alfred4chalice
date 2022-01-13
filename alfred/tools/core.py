import re


def only_digits(value: str):
    return "".join(filter(lambda i: i.isdigit(), value))


def has_accent(value):
    reg = "[\u00C0-\u00FF]"
    return bool(re.search(reg, value))


def is_email_valid(value):
    reg = r"^([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)$"  # noqa: E501
    return bool(re.match(reg, value))
