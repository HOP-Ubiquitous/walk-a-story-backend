from typing import List
from places.dto import PointOfInterestDto, CityDto


class PlaceService:
    def add_city(self, name, points_of_interest) -> CityDto:
        raise NotImplementedError('you must implement this method')

    def get_city(self, id) -> CityDto:
        raise NotImplementedError('you must implement this method')

    def get_city_by_point_of_interest_id(self, id) -> [CityDto]:
        raise NotImplementedError('you must implement this method')

    def delete_city(self, id) -> CityDto:
        raise NotImplementedError('you must implement this method')

    def get_all_cities(self) -> List[CityDto]:
        raise NotImplementedError('you must implement this method')

    def update_city(self, id, name) -> CityDto:
        raise NotImplementedError('you must implement this method')

    def add_point_of_interest(self, name, city_id, latitude, longitude) -> PointOfInterestDto:
        raise NotImplementedError('you must implement this method')

    def delete_point_of_interest(self, id) -> PointOfInterestDto:
        raise NotImplementedError('you must implement this method')

    def get_all_points_of_interest(self) -> List[PointOfInterestDto]:
        raise NotImplementedError('you must implement this method')

    def get_point_of_interest_by_id(self, id) -> PointOfInterestDto:
        raise NotImplementedError('you must implement this method')

    def get_points_of_interest_by_city_id(self, id) -> List[PointOfInterestDto]:
        raise NotImplementedError('you must implement this method')

    def update_point_of_interest(self, id, name, city_id, latitude, longitude) -> PointOfInterestDto:
        raise NotImplementedError('you must implement this method')
