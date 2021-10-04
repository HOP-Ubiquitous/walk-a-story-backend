class CommentsError(Exception):
    def __init__(self, message, status, *args):
        super(CommentsError, self).__init__(message, *args)
        self.status = status
