from typing import List

from caminatas.entities.caminata import Caminata


class CaminataStore:
    def add(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
            participants) -> Caminata:
        raise NotImplementedError('you must implement this method')

    def get_caminata_by_id(self, caminata_id) -> Caminata:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[Caminata]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_user(self, user_id) -> List[Caminata]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_participant_user(self, user_id) -> List[Caminata]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_place(self, place_id) -> List[Caminata]:
        raise NotImplementedError('you must implement this method')

    def update(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude,
               user_id) -> Caminata:
        raise NotImplementedError('you must implement this method')

    def put_participant(self, caminata_id, user_id) -> Caminata:
        raise NotImplementedError('you must implement this method')

    def delete_participant(self, caminata_id, user_id) -> Caminata:
        raise NotImplementedError('you must implement this method')

    def delete(self, caminata_id) -> Caminata:
        raise NotImplementedError('you must implement this method')
