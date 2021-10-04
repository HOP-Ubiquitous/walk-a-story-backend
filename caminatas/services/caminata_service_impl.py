import uuid
from typing import List
from dateutil.parser import parse

from caminatas import mapper
from caminatas.dto import CaminataDto
from caminatas.services.caminata_service import CaminataService
from caminatas.stores.caminata_store import CaminataStore


class CaminataServiceImpl(CaminataService):
    def __init__(self, caminata_store: CaminataStore):
        self.caminata_store = caminata_store

    def add(self, title, description, date, image, place_id, address, latitude, longitude, user_id,
            participants) -> CaminataDto:
        caminata_entity = self.caminata_store.add(str(uuid.uuid4()),
                                                  title,
                                                  description,
                                                  parse(date),
                                                  image,
                                                  place_id,
                                                  address,
                                                  latitude,
                                                  longitude,
                                                  user_id,
                                                  participants)
        return mapper.to_dto(caminata_entity)

    def get_caminata_by_id(self, caminata_id) -> CaminataDto:
        caminata_entity = self.caminata_store.get_caminata_by_id(caminata_id)
        return mapper.to_dto(caminata_entity)

    def get_all(self) -> List[CaminataDto]:
        caminata_entities = self.caminata_store.get_all()
        return [mapper.to_dto(caminata_entity) for caminata_entity in caminata_entities]

    def get_caminatas_by_user(self, user_id) -> List[CaminataDto]:
        caminata_entities = self.caminata_store.get_caminatas_by_user(user_id)
        return [mapper.to_dto(caminata_entity) for caminata_entity in caminata_entities]

    def get_caminatas_by_participant_user(self, user_id) -> List[CaminataDto]:
        caminata_entities = self.caminata_store.get_caminatas_by_participant_user(user_id)
        return [mapper.to_dto(caminata_entity) for caminata_entity in caminata_entities]

    def get_caminatas_by_place(self, place_id) -> List[CaminataDto]:
        caminata_entities = self.caminata_store.get_caminatas_by_place(place_id)
        return [mapper.to_dto(caminata_entity) for caminata_entity in caminata_entities]

    def update(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
               participants) -> CaminataDto:
        caminata_entity = self.caminata_store.update(caminata_id,
                                                     title,
                                                     description,
                                                     parse(date),
                                                     image,
                                                     place_id,
                                                     address,
                                                     latitude,
                                                     longitude,
                                                     user_id)
        return mapper.to_dto(caminata_entity)

    def put_participant(self, caminata_id, user_id):
        caminata_entity = self.caminata_store.put_participant(caminata_id, user_id)
        return mapper.to_dto(caminata_entity)

    def delete_participant(self, caminata_id, user_id):
        caminata_entity = self.caminata_store.delete_participant(caminata_id, user_id)
        return mapper.to_dto(caminata_entity)

    def delete(self, caminata_id) -> CaminataDto:
        caminata_entity = self.caminata_store.delete(caminata_id)
        return mapper.to_dto(caminata_entity)

    def update_dto(self, caminata_dto: CaminataDto) -> CaminataDto:
        caminata_entity = self.caminata_store.update(caminata_dto.caminata_id(),
                                                     caminata_dto.title,
                                                     caminata_dto.description,
                                                     caminata_dto.date,
                                                     caminata_dto.image,
                                                     caminata_dto.place_id,
                                                     caminata_dto.address,
                                                     caminata_dto.latitude,
                                                     caminata_dto.longitude,
                                                     caminata_dto.user)
        return mapper.to_dto(caminata_entity)
