from typing import List
from locations.dto import LocationDto


class LocationService:
    def add(self, is_active, type, subtype, title, description, coordinates, workers,
            owner_user_id, main_video_id) -> LocationDto:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[LocationDto]:
        raise NotImplementedError('you must implement this method')

    def get(self, location_id) -> LocationDto:
        raise NotImplementedError('you must implement this method')

    def get_by_type(self, type) -> List[LocationDto]:
        raise NotImplementedError('you must implement this method')

    def get_by_owner_user_id(self, user_id) -> List[LocationDto]:
        raise NotImplementedError('you must implement this method')

    def get_by_params(self, params) -> List[LocationDto]:
        raise NotImplementedError('you must implement this method')

    def put_active(self, location_id):
        raise NotImplementedError('you must implement this method')

    def put_inactive(self, location_id):
        raise NotImplementedError('you must implement this method')

    def update(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
               owner_user_id, main_video_id) -> LocationDto:
        raise NotImplementedError('you must implement this method')

    def delete(self, location_id) -> LocationDto:
        raise NotImplementedError('you must implement this method')
