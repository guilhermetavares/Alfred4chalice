def only_digits(value: str):
    return "".join(filter(lambda i: i.isdigit(), value))
