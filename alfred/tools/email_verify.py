import requests

APPROVE_LIST = [
    "ok",
    "unknown",
    "key_not_valid",
    "missing parameter",
]

class EmailListVerifyOne():
    def __init__(self, key, email):
        self.key = key
        self.email = email
        self.base_url = "https://apps.emaillistverify.com/api/verifyEmail?secret="
        self.url = self.base_url+self.key+"&email="+self.email

    def control(self):
        response = requests.get(self.url)
        return response.text

    def verify(self):
        try:
            control = self.control()
        except:
            return True
        
        return True if control in APPROVE_LIST else False