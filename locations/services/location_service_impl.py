import uuid
from datetime import datetime
from typing import List

from flask_login import current_user

from locations import mapper
from locations.dto import LocationDto
from locations.services.location_service import LocationService
from locations.stores.location_store import LocationStore


class LocationServiceImpl(LocationService):
    def __init__(self, location_store: LocationStore, is_secure_api = False):
        self.location_store = location_store
        self.is_secure_api = is_secure_api

    def add(self, is_active, type, subtype, title, description, coordinates, workers,
            owner_user_id, main_video_id) -> LocationDto:
        location_entity = self.location_store.add(
            str(uuid.uuid4()),
            is_active,
            type,
            subtype,
            title,
            description,
            coordinates.latitude,
            coordinates.longitude,
            workers,
            owner_user_id,
            main_video_id,
            datetime.utcnow()
        )
        return mapper.to_dto(location_entity)

    def get_all(self) -> List[LocationDto]:
        location_entities = self.location_store.get_all()
        return [mapper.to_dto(location_entity) for location_entity in location_entities]

    def get(self, location_id) -> LocationDto:
        location_entity = self.location_store.get(location_id)
        return mapper.to_dto(location_entity)

    def get_by_type(self, type) -> List[LocationDto]:
        location_entities = self.location_store.get_by_type(type)
        return [mapper.to_dto(location_entity) for location_entity in location_entities]

    def get_by_owner_user_id(self, user_id) -> List[LocationDto]:
        location_entities = self.location_store.get_by_owner_user_id(user_id)
        return [mapper.to_dto(location_entity) for location_entity in location_entities]

    def get_by_params(self, params) -> List[LocationDto]:
        location_entities = self.location_store.get_by_params(params)
        return [mapper.to_dto(location_entity) for location_entity in location_entities]

    def put_active(self, location_id):
        location_entity = self.location_store.get(location_id)
        location_dto = mapper.to_dto(location_entity)
        location_dto.is_active = True
        return self._update(location_dto)

    def put_inactive(self, location_id):
        location_entity = self.location_store.get(location_id)
        location_dto = mapper.to_dto(location_entity)
        location_dto.is_active = False
        return self._update(location_dto)

    def update(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
               owner_user_id, main_video_id) -> LocationDto:
        if not self.is_secure_api or self._is_current_user_admin_or_owner(location_id):
            location_dto = self.get(location_id)
            if location_dto is not LocationDto.NULL:
                location_dto.is_active = is_active
                location_dto.type = type
                location_dto.subtype = subtype
                location_dto.title = title
                location_dto.description = description
                location_dto.coordinates.latitude = latitude
                location_dto.coordinates.longitude = longitude
                location_dto.workers = workers
                location_dto.owner_user_id = owner_user_id
                location_dto.main_video_id = main_video_id
                return self._update(location_dto)
            else:
                return LocationDto.NULL
        else:
            return LocationDto.NULL

    def _update(self, location_dto) -> LocationDto:
        if not self.is_secure_api or self._is_current_user_admin_or_owner(location_dto.location_id()):
            location_entity = self.location_store.update(location_dto.location_id(),
                                                         location_dto.is_active,
                                                         location_dto.type,
                                                         location_dto.subtype,
                                                         location_dto.title,
                                                         location_dto.description,
                                                         location_dto.coordinates.latitude,
                                                         location_dto.coordinates.longitude,
                                                         location_dto.workers,
                                                         location_dto.owner_user_id,
                                                         location_dto.main_video_id,
                                                         location_dto.creation_date)
            return mapper.to_dto(location_entity)
        else:
            return LocationDto.NULL

    def delete(self, location_id) -> LocationDto:
        if not self.is_secure_api or self._is_current_user_admin_or_owner(location_id):
            location_entity = self.location_store.delete(location_id)
            return mapper.to_dto(location_entity)
        else:
            return LocationDto.NULL

    def _is_current_user_admin_or_owner(self, location_id):
        location_entity = self.location_store.get(location_id)
        return current_user.is_active and (current_user.admin or current_user.id == location_entity.owner_user_id)
