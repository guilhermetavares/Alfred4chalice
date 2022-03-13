import random

import requests

from alfred.settings import ALFRED_EMAIL_VERIFY_RATE, ALFRED_EMAIL_VERIFY_TOKEN

from .core import is_email_valid

APPROVE_LIST = [
    "ok",
    "unknown",
    "key_not_valid",
    "missing parameter",
]


class EmailListVerifyOne:
    BASE_URL = (
        "https://apps.emaillistverify.com/api/verifyEmail?secret={secret}&email={email}"
    )

    @classmethod
    def control(self, email):
        url_ = self.BASE_URL.format(email=email, secret=ALFRED_EMAIL_VERIFY_TOKEN)
        return requests.get(url_).text

    @classmethod
    def verify(self, email):
        try:
            control = self.control(email)
        except Exception:
            return True
        return True if control in APPROVE_LIST else False


def is_smtp_email_valid(email, force=False):
    if is_email_valid(email):
        if force or int(random.uniform(0, 100)) < int(ALFRED_EMAIL_VERIFY_RATE):
            return EmailListVerifyOne.verify(email)
        return True
    return False
