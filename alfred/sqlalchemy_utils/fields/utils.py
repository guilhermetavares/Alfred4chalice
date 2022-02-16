import hashlib

from alfred.settings import ALFRED_PASSWORD_SALT


def hash_password(raw_password, salt=None, interations=100000):
    value_encode = raw_password.encode()

    salt_encode = salt.encode() if salt else ALFRED_PASSWORD_SALT.encode()
    password = hashlib.pbkdf2_hmac(
        "sha512", value_encode, salt_encode, interations
    ).hex()
    return password
