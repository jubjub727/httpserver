class HTTPResponse:
    contentType = "text/html"
    code = None
    reason = None
    headers = {}
    message = None

    def __init__(self, code, message=None):
        self.code = code
        self.message = message
