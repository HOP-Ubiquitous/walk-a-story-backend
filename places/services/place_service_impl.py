from typing import List

from caminatas.services.caminata_service import CaminataService
from places import mapper
from places.dto import CityDto, PointOfInterestDto
from places.entities.city import City
from places.places_error import PlacesError
from places.services.place_service import PlaceService
from places.stores.city_store import CityStore
from places.stores.point_of_interest_store import PointOfInterestStore
from video_catalog.services.video_service import VideoService


class PlaceServiceImpl(PlaceService):
    def __init__(self, city_store: CityStore,
                 point_of_interest_store: PointOfInterestStore,
                 caminatas_service: CaminataService,
                 video_service: VideoService):
        self.city_store = city_store
        self.point_of_interest_store = point_of_interest_store
        self.caminatas_service = caminatas_service
        self.video_service = video_service

    def add_city(self, name, points_of_interest) -> CityDto:
        city_entity = self.city_store.add(name, points_of_interest)
        return mapper.city_to_dto(city_entity)

    def get_city(self, id):
        city_entity = self.city_store.get(id)
        return mapper.city_to_dto(city_entity)

    def get_city_by_point_of_interest_id(self, id) -> List[CityDto]:
        city_entities = self.city_store.get_by_point_of_interest_id(id)
        return [mapper.city_to_dto(city_entity) for city_entity in city_entities]

    def delete_city(self, id) -> CityDto:
        city_entity = self.city_store.get(id)
        if len(city_entity.points_of_interest) > 0:
            return CityDto.NULL
        city_entity = self.city_store.delete(id)
        return mapper.city_to_dto(city_entity)

    def get_all_cities(self) -> List[CityDto]:
        city_entities = self.city_store.get_all()
        return [mapper.city_to_dto(city_entity) for city_entity in city_entities]

    def update_city(self, id, name) -> CityDto:
        city_entity = self.city_store.update(id, name)
        return mapper.city_to_dto(city_entity)

    def add_point_of_interest(self, name, city_id, latitude, longitude) -> PointOfInterestDto:
        city = self.city_store.get(city_id)
        if city is City.NULL:
            return PointOfInterestDto.NULL
        point_of_interest = self.point_of_interest_store.add(name, city, latitude, longitude)
        return mapper.point_of_interest_to_dto(point_of_interest)

    def delete_point_of_interest(self, id) -> PointOfInterestDto:
        caminatas_dto = self.caminatas_service.get_caminatas_by_place(id)
        videos_dto = self.video_service.get_videos_by_place(id)
        if len(caminatas_dto) > 0 or len(videos_dto) > 0:
            raise(PlacesError('items associated to this point', 400))
        point_of_interest = self.point_of_interest_store.delete(id)
        return mapper.point_of_interest_to_dto(point_of_interest)

    def get_all_points_of_interest(self) -> List[PointOfInterestDto]:
        points_of_interest = self.point_of_interest_store.get_all()
        return [mapper.point_of_interest_to_dto(point_of_interest) for point_of_interest in points_of_interest]

    def get_point_of_interest_by_id(self, id) -> PointOfInterestDto:
        point_of_interest = self.point_of_interest_store.get(id)
        return mapper.point_of_interest_to_dto(point_of_interest)

    def get_points_of_interest_by_city_id(self, id) -> List[PointOfInterestDto]:
        points_of_interest = self.point_of_interest_store.get_by_city_id(id)
        return [mapper.point_of_interest_to_dto(point_of_interest) for point_of_interest in points_of_interest]

    def update_point_of_interest(self, id, name, city_id, latitude, longitude) -> PointOfInterestDto:
        city = self.city_store.get(city_id)
        if city is City.NULL:
            raise(PlacesError('city_id was not found', 400))
        point_ofr_interest = self.point_of_interest_store.update(id, name, city_id, latitude, longitude)
        return mapper.point_of_interest_to_dto(point_ofr_interest)
