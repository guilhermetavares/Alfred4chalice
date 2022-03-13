import requests
from alfred.settings import ALFRED_EMAIL_VERIFY_TOKEN


APPROVE_LIST = [
    "ok",
    "unknown",
    "key_not_valid",
    "missing parameter",
]

class EmailListVerifyOne():
    def __init__(self):
        self.key = ALFRED_EMAIL_VERIFY_TOKEN
        self.base_url = "https://apps.emaillistverify.com/api/verifyEmail?secret="
        self.url = self.base_url+self.key+"&email="

    def control(self, email):
        response = requests.get(self.url+email)
        return response.text

    def verify(self, email):
        try:
            control = self.control(email)
        except:
            return True

        return True if control in APPROVE_LIST else False