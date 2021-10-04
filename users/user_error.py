class UserError(Exception):
    def __init__(self, message, status, *args):
        super(UserError, self).__init__(message, *args)
        self.status = status
