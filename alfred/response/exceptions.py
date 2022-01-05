class ResponseError(Exception):
    def __init__(self, status_code, message, send_to_sentry=False, extra=None):
        self.status_code = status_code
        self.body = {"error": [message]}
        if extra:
            self.body["_error_extra"] = extra
        self.send_to_sentry = send_to_sentry
        super().__init__(message)
