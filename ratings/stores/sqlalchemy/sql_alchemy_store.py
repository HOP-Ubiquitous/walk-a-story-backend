from typing import List
import colorlog
from sqlalchemy.orm import Session

from ratings.entities.rating import Rating
from ratings.stores.rating_store import RatingStore
from ratings.stores.sqlalchemy import mapper
from ratings.stores.sqlalchemy.data_access_layer import DataAccessLayer
from ratings.stores.sqlalchemy.models import RatingModel

logger = colorlog.getLogger('SQLAlchemyRatingStore')


class SQLAlchemyRatingStore(RatingStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()
        return super().__new__(cls)

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyRatingStore.dal.Session()

    def get_by_user_id(self, user_id):
        session = SQLAlchemyRatingStore.get_session()
        rating_models = session.query(RatingModel).filter_by(user_id=user_id)
        logger.debug("Collected {} ratings".format(user_id))
        return mapper.query_rating_model_to_entity_list(rating_models)

    def add(self, rating_id, associated_id, associated_type, user_id, rating_type, date, value) -> Rating:
        session = SQLAlchemyRatingStore.get_session()
        rating_model = RatingModel(
            id=rating_id,
            associated_id=associated_id,
            associated_type=associated_type,
            user_id=user_id,
            rating_type=rating_type,
            date=date,
            value=value
        )
        session.add(rating_model)
        session.commit()
        session.refresh(rating_model)

        logger.debug("Added: {}".format(rating_model))
        return mapper.rating_model_to_entity(rating_model)

    def get(self, rating_id) -> Rating:
        session = SQLAlchemyRatingStore.get_session()
        rating_model = session.query(RatingModel).get(rating_id)
        logger.debug("Collected: {}".format(rating_model))
        return Rating.NULL if rating_model is None else mapper.rating_model_to_entity(rating_model)

    def get_all(self) -> List[Rating]:
        session = SQLAlchemyRatingStore.get_session()
        rating_models = session.query(RatingModel)
        logger.debug("Collected all ratings")
        return mapper.query_rating_model_to_entity_list(rating_models)

    def get_by_associated_id_by_associated_type_by_rating_type_by_user_id(self, associated_id, associated_type,
                                                                          rating_type, user_id) -> List[Rating]:
        session = SQLAlchemyRatingStore.get_session()
        rating_models = session.query(RatingModel).filter_by(associated_id=associated_id,
                                                             associated_type=associated_type,
                                                             rating_type=rating_type,
                                                             user_id=user_id)
        logger.debug("Collected ratings")
        return mapper.query_rating_model_to_entity_list(rating_models)

    def delete(self, rating_id) -> Rating:
        session = SQLAlchemyRatingStore.get_session()
        rating_model = session.query(RatingModel).get(rating_id)
        if rating_model:
            session.delete(rating_model)
            session.commit()
            logger.debug("Deleted: {}".format(rating_model))
            return mapper.rating_model_to_entity(rating_model)
        return Rating.NULL
