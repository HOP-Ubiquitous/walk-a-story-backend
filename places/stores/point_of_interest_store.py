from typing import List
from places.entities.point_of_interest import PointOfInterest


class PointOfInterestStore:

    def add(self, name, city, latitude, longitude) -> PointOfInterest:
        raise NotImplementedError('you must implement this method')

    def delete(self, id) -> PointOfInterest:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[PointOfInterest]:
        raise NotImplementedError('you must implement this method')

    def get(self, id) -> PointOfInterest:
        raise NotImplementedError('you must implement this method')

    def get_by_city_id(self, id) -> List[PointOfInterest]:
        raise NotImplementedError('you must implement this method')

    def update(self, id, name, city, latitude, longitude) -> PointOfInterest:
        raise NotImplementedError('you must implement this method')
