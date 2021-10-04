class RatingsError(Exception):
    def __init__(self, message, status, *args):
        super(RatingsError, self).__init__(message, *args)
        self.status = status
