class EFException:
    def __init__(self):
        self.status_code = 0
        self.message = ''


class EFBadRequestException(Exception):
    def __init__(self, message):
        self.status_code = 400
        self.message = message
        super().__init__(self.message)


class EFAuthException(Exception):
    def __init__(self, message):
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class EFServerException(Exception):
    def __init__(self, message):
        self.status_code = 500
        self.message = message
        super().__init__(self.message)
