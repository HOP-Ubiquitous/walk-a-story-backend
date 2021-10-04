from utils.null_object import Null


class PointOfInterest:
    NULL = Null()

    def __init__(self, id, name, city_id, latitude, longitude):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
