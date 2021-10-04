import json
from utils.null_object import Null


class CityDto:
    NULL = Null()

    def __init__(self, id, name, points_of_interest):
        self.id = id
        self.name = name
        self.points_of_interest = points_of_interest

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'points_of_interest': [
                point_of_interest.to_dict()
                for point_of_interest in self.points_of_interest
            ]
        }


class PointOfInterestDto:
    NULL = Null()

    def __init__(self, id, name, city_id, latitude, longitude):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
