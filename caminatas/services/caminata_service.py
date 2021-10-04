from typing import List
from caminatas.dto import CaminataDto


class CaminataService:
    def add(self, title, description, date, image, place_id, address, latitude, longitude, user_id,
            participants) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def get_caminata_by_id(self, caminata_id) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[CaminataDto]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_user(self, user_id) -> List[CaminataDto]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_participant_user(self, user_id) -> List[CaminataDto]:
        raise NotImplementedError('you must implement this method')

    def get_caminatas_by_place(self, place_id) -> List[CaminataDto]:
        raise NotImplementedError('you must implement this method')

    def update(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
               participants) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def put_participant(self, caminata_id, user_id) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def delete_participant(self, caminata_id, user_id) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def delete(self, caminata_id) -> CaminataDto:
        raise NotImplementedError('you must implement this method')

    def update_dto(self, caminata_dto: CaminataDto) -> CaminataDto:
        raise NotImplementedError('you must implement this method')
