class PlacesError(Exception):
    def __init__(self, message, status, *args):
        super(PlacesError, self).__init__(message, *args)
        self.status = status
