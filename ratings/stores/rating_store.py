from typing import List
from ratings.entities.rating import Rating


class RatingStore:

    def get_by_user_id(self, user_id):
        raise NotImplementedError('you must implement this method')

    def add(self, rating_id, associated_id, associated_type, user_id, rating_type, date, value) -> Rating:
        raise NotImplementedError('you must implement this method')

    def get(self, rating_id) -> Rating:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[Rating]:
        raise NotImplementedError('you must implement this method')

    def get_by_associated_id_by_associated_type_by_rating_type_by_user_id(self, associated_id, associated_type,
                                                                          rating_type, user_id) -> List[Rating]:
        raise NotImplementedError('you must implement this method')

    def delete(self, rating_id) -> Rating:
        raise NotImplementedError('you must implement this method')
