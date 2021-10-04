class LocationsError(Exception):
    def __init__(self, message, status, *args):
        super(LocationsError, self).__init__(message, *args)
        self.status = status
