from typing import List

from locations.entities.location import Location


class LocationStore:
    def add(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
            owner_user_id, main_video_id, creation_date) -> Location:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[Location]:
        raise NotImplementedError('you must implement this method')

    def get(self, location_id) -> Location:
        raise NotImplementedError('you must implement this method')

    def get_by_type(self, type) -> List[Location]:
        raise NotImplementedError('you must implement this method')

    def get_by_owner_user_id(self, user_id) -> List[Location]:
        raise NotImplementedError('you must implement this method')

    def get_by_params(self, params) -> List[Location]:
        raise NotImplementedError('you must implement this method')

    def update(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
               owner_user_id, main_video_id, creation_date) -> Location:
        raise NotImplementedError('you must implement this method')

    def delete(self, location_id) -> Location:
        raise NotImplementedError('you must implement this method')
