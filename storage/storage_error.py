class StorageError(Exception):
    def __init__(self, message, status, *args):
        super(StorageError, self).__init__(message, *args)
        self.status = status
