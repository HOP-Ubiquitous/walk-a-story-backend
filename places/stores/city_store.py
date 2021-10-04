from typing import List

from places.entities.city import City


class CityStore:
    def add(self, name, points_of_interest) -> City:
        raise NotImplementedError('you must implement this method')

    def get(self, id) -> City:
        raise NotImplementedError('you must implement this method')

    def get_by_point_of_interest_id(self, id) -> List[City]:
        raise NotImplementedError('you must implement this method')

    def delete(self, id) -> City:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[City]:
        raise NotImplementedError('you must implement this method')

    def update(self, id, name) -> City:
        raise NotImplementedError('you must implement this method')
