from typing import List
import colorlog
from sqlalchemy.orm import Session

from places.entities.point_of_interest import PointOfInterest
from places.stores.point_of_interest_store import PointOfInterestStore
from places.stores.sqlalchemy.models import PointOfInterestModel, CityModel
from places.stores.sqlalchemy import mapper
from places.stores.sqlalchemy.data_access_layer import DataAccessLayer

logger = colorlog.getLogger('SQLAlchemyPointOfInterestStore')


class SQLAlchemyPointOfInterestStore(PointOfInterestStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    def add(self, name, city, latitude, longitude) -> PointOfInterest:
        session = SQLAlchemyPointOfInterestStore.get_session()
        # city_model = session.query(CityModel).get(city.id)

        point_of_interest_model = PointOfInterestModel(
            name=name,
            city_id=city.id,
            latitude=latitude,
            longitude=longitude
        )

        # city_model.points_of_interest.append(point_of_interest_model)

        session.add(point_of_interest_model)
        # session.add(city_model)
        session.commit()
        session.refresh(point_of_interest_model)
        # session.refresh(city_model)

        logger.debug("Added: {}".format(point_of_interest_model))
        point_of_interest = mapper.point_of_interest_model_to_entity(point_of_interest_model)
        return point_of_interest

    def delete(self, id) -> PointOfInterest:
        session = SQLAlchemyPointOfInterestStore.get_session()
        point_of_interest_model = session.query(PointOfInterestModel).get(id)
        if point_of_interest_model:
            session.delete(point_of_interest_model)
            session.commit()
            logger.debug("Deleted: {}".format(point_of_interest_model))
            return mapper.point_of_interest_model_to_entity(point_of_interest_model)
        return PointOfInterest.NULL

    def get_all(self) -> List[PointOfInterest]:
        session = SQLAlchemyPointOfInterestStore.get_session()
        point_of_interest_model = session.query(PointOfInterestModel)
        logger.debug("Collected all point of interest")
        print(point_of_interest_model.all())
        return mapper.query_point_of_interest_model_to_entity_list(point_of_interest_model)

    def get(self, id) -> PointOfInterest:
        session = SQLAlchemyPointOfInterestStore.get_session()
        point_of_interest_model = session.query(PointOfInterestModel).get(id)
        logger.debug("Collected: {}".format(point_of_interest_model))
        return PointOfInterest.NULL if point_of_interest_model is None else mapper.point_of_interest_model_to_entity(
            point_of_interest_model)

    def get_by_city_id(self, id) -> List[PointOfInterest]:
        session = SQLAlchemyPointOfInterestStore.get_session()
        point_of_interest_model = session.query(PointOfInterestModel).filter_by(city_id=id)
        logger.debug("Collected: {}".format(point_of_interest_model))
        return PointOfInterest.NULL if point_of_interest_model is None else mapper. \
            query_point_of_interest_model_to_entity_list(point_of_interest_model)

    def update(self, id, name, city_id, latitude, longitude) -> PointOfInterest:
        session = SQLAlchemyPointOfInterestStore.get_session()
        point_of_interest_model = session.query(PointOfInterestModel).get(id)
        if point_of_interest_model is None:
            return PointOfInterest.NULL

        point_of_interest_model.name = name
        point_of_interest_model.city_id = city_id
        point_of_interest_model.latitude = latitude
        point_of_interest_model.longitude = longitude

        session.merge(point_of_interest_model)
        session.commit()
        session.refresh(point_of_interest_model)

        logger.debug("Updated: {}".format(point_of_interest_model))
        return mapper.point_of_interest_model_to_entity(point_of_interest_model)

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyPointOfInterestStore.dal.Session()
