from typing import List
import colorlog
from sqlalchemy.orm import Session, contains_eager

from places.entities.city import City
from places.stores.city_store import CityStore
from places.stores.sqlalchemy import mapper
from places.stores.sqlalchemy.data_access_layer import DataAccessLayer
from places.stores.sqlalchemy.models import CityModel, PointOfInterestModel

logger = colorlog.getLogger('SQLAlchemyCityStore')


class SQLAlchemyCityStore(CityStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    def add(self, name, points_of_interest) -> City:
        session = SQLAlchemyCityStore.get_session()
        city_model = CityModel(name=name, points_of_interest=points_of_interest)

        try:
            session.add(city_model)
            session.commit()
            session.refresh(city_model)
        except Exception:
            return City.NULL

        logger.debug("Added: {}".format(city_model))
        city = mapper.city_model_to_entity(city_model)

        return city

    def get(self, id) -> City:
        session = SQLAlchemyCityStore.get_session()
        city_model = session.query(CityModel).get(id)
        if city_model:
            return mapper.city_model_to_entity(city_model)
        return City.NULL

    def get_by_point_of_interest_id(self, id) -> List[City]:
        session = SQLAlchemyCityStore.get_session()
        city_models = session.query(CityModel).join(CityModel.points_of_interest).filter(PointOfInterestModel.id == id)
        logger.debug("Collected cities:".format(city_models))
        return City.NULL if city_models is None else mapper.query_city_model_to_entity_list(city_models)

    def delete(self, id) -> City:
        session = SQLAlchemyCityStore.get_session()
        city_model = session.query(CityModel).get(id)

        if city_model:
            session.delete(city_model)
            session.commit()
            logger.debug("Deleted: {}".format(city_model))
            return mapper.city_model_to_entity(city_model)

        return City.NULL

    def get_all(self) -> List[City]:
        session = SQLAlchemyCityStore.get_session()
        cities_model = session.query(CityModel)
        logger.debug("Collected all cities")
        print(cities_model.all())

        return mapper.query_city_model_to_entity_list(cities_model)

    def update(self, id, name) -> City:
        session = SQLAlchemyCityStore.get_session()
        city_model: CityModel = session.query(CityModel).get(id)
        if city_model is None:
            return City.NULL

        city_model.name = name

        session.merge(city_model)
        session.commit()
        session.refresh(city_model)

        logger.debug("Updated: {}".format(city_model))
        return mapper.city_model_to_entity(city_model)

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyCityStore.dal.Session()
