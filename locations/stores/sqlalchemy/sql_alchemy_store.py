from typing import List
import colorlog
from sqlalchemy.orm import Session

from locations.entities.location import Location
from locations.stores.sqlalchemy.models import LocationModel
from locations.stores.location_store import LocationStore
from locations.stores.sqlalchemy import mapper
from locations.stores.sqlalchemy.data_access_layer import DataAccessLayer

logger = colorlog.getLogger('SQLAlchemyLocationStore')


class SQLAlchemyLocationStore(LocationStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    def add(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
            owner_user_id, main_video_id, creation_date) -> Location:
        session = SQLAlchemyLocationStore.get_session()
        location_model = LocationModel(id=str(location_id),
                                       is_active=is_active,
                                       type=type,
                                       subtype=subtype,
                                       title=title,
                                       description=description,
                                       latitude=latitude,
                                       longitude=longitude,
                                       workers=workers,
                                       owner_user_id=owner_user_id,
                                       main_video_id=main_video_id,
                                       creation_date=creation_date)

        session.add(location_model)
        session.commit()
        session.refresh(location_model)

        logger.debug("Added: {}".format(location_model))
        location = mapper.location_model_to_entity(location_model)
        return location

    def get_all(self) -> List[Location]:
        session = SQLAlchemyLocationStore.get_session()
        locations = session.query(LocationModel)
        logger.debug("Collected all locations")
        return mapper.query_location_model_to_entity_list(locations)

    def get(self, location_id) -> Location:
        session = SQLAlchemyLocationStore.get_session()
        location = session.query(LocationModel).get(location_id)
        logger.debug("Collected: {}".format(location))
        return Location.NULL if location is None else mapper.location_model_to_entity(location)

    def get_by_type(self, type) -> List[Location]:
        session = SQLAlchemyLocationStore.get_session()
        location = session.query(LocationModel).filter_by(type=type)
        logger.debug("Collected: {}".format("location where type: " + str(type)))
        return mapper.query_location_model_to_entity_list(location)

    def get_by_owner_user_id(self, user_id) -> List[Location]:
        session = SQLAlchemyLocationStore.get_session()
        location = session.query(LocationModel).filter_by(owner_user_id=user_id)
        logger.debug("Collected: {}".format("location where owner_user_id: " + str(user_id)))
        return mapper.query_location_model_to_entity_list(location)

    def get_by_params(self, params) -> List[Location]:
        session = SQLAlchemyLocationStore.get_session()
        location = session.query(LocationModel).filter_by(**params)
        logger.debug(f'Collected: {location} with filter_by: {params}')
        return mapper.query_location_model_to_entity_list(location)

    def update(self, location_id, is_active, type, subtype, title, description, latitude, longitude, workers,
               owner_user_id, main_video_id, creation_date) -> Location:
        session = SQLAlchemyLocationStore.get_session()
        location_model: LocationModel = session.query(LocationModel).get(location_id)
        if location_model is None:
            return Location.NULL

        location_model.is_active = is_active
        location_model.type = type
        location_model.subtype = subtype
        location_model.title = title
        location_model.description = description
        location_model.latitude = latitude
        location_model.longitude = longitude
        location_model.workers = workers
        location_model.owner_user_id = owner_user_id
        location_model.main_video_id = main_video_id
        location_model.creation_date = creation_date

        session.merge(location_model)
        session.commit()
        session.refresh(location_model)

        logger.debug("Updated: {}".format(location_model))
        return mapper.location_model_to_entity(location_model)

    def delete(self, location_id) -> Location:
        session = SQLAlchemyLocationStore.get_session()
        location = session.query(LocationModel).get(location_id)
        if location:
            session.delete(location)
            session.commit()
            logger.debug("Deleted: {}".format(location))
            return mapper.location_model_to_entity(location)
        return Location.NULL

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyLocationStore.dal.Session()
