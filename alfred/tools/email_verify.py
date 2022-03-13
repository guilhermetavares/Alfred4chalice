import requests

from alfred.settings import ALFRED_EMAIL_VERIFY_TOKEN

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

    def control(self, email):
        url_ = self.BASE_URL.format(email=email, secret=ALFRED_EMAIL_VERIFY_TOKEN)
        response = requests.get(url_)
        return response.text

    def verify(self, email):
        try:
            control = self.control(email)
        except Exception:
            return True

        return True if control in APPROVE_LIST else False
