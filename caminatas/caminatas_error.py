class CaminatasError(Exception):
    def __init__(self, message, status, *args):
        super(CaminatasError, self).__init__(message, *args)
        self.status = status
