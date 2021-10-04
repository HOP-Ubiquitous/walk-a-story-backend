from typing import List
import colorlog
from sqlalchemy.orm import Session

from caminatas.entities.caminata import Caminata
from caminatas.stores.sqlalchemy.models import CaminataModel
from caminatas.stores.caminata_store import CaminataStore
from caminatas.stores.sqlalchemy import mapper
from caminatas.stores.sqlalchemy.data_access_layer import DataAccessLayer

logger = colorlog.getLogger('SQLAlchemyCaminataStore')


class SQLAlchemyCaminataStore(CaminataStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    def add(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
            participants) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata_model = CaminataModel(id=str(caminata_id),
                                       title=title,
                                       description=description,
                                       date=date,
                                       image=image,
                                       place_id=place_id,
                                       address=address,
                                       latitude=latitude,
                                       longitude=longitude,
                                       user_id=user_id,
                                       participants=participants)

        session.add(caminata_model)
        session.commit()
        session.refresh(caminata_model)

        logger.debug("Added: {}".format(caminata_model))
        caminata = mapper.caminata_model_to_entity(caminata_model)

        return caminata

    def get_caminata_by_id(self, caminata_id) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata = session.query(CaminataModel).get(caminata_id)
        logger.debug("Collected: {}".format(caminata))
        return Caminata.NULL if caminata is None else mapper.caminata_model_to_entity(caminata)

    def get_all(self) -> List[Caminata]:
        session = SQLAlchemyCaminataStore.get_session()
        caminatas = session.query(CaminataModel)
        logger.debug("Collected all caminatas")
        return mapper.query_caminata_model_to_entity_list(caminatas)

    def get_caminatas_by_user(self, user_id) -> List[Caminata]:
        session = SQLAlchemyCaminataStore.get_session()
        caminatas = session.query(CaminataModel).filter_by(user_id=user_id)
        logger.debug("Collected: {}".format("caminatas where user_id: " + str(user_id)))
        return mapper.query_caminata_model_to_entity_list(caminatas)

    def get_caminatas_by_participant_user(self, user_id) -> List[Caminata]:
        session = SQLAlchemyCaminataStore.get_session()
        # caminatas = session.query(CaminataModel).filter_by(participant=user_id)
        caminatas = session.query(CaminataModel).filter(CaminataModel.participants.contains(user_id))
        logger.debug("Collected: {}".format("caminatas where participant user_id: " + str(user_id)))
        return mapper.query_caminata_model_to_entity_list(caminatas)

    def get_caminatas_by_place(self, place_id) -> List[Caminata]:
        session = SQLAlchemyCaminataStore.get_session()
        caminatas = session.query(CaminataModel).filter_by(place_id=place_id)
        logger.debug("Collected: {}".format("caminatas where place_id: " + place_id))
        return mapper.query_caminata_model_to_entity_list(caminatas)

    def update(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude,
               user_id) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata_model: CaminataModel = session.query(CaminataModel).get(caminata_id)
        if caminata_model is None:
            return Caminata.NULL

        caminata_model.title = title
        caminata_model.description = description
        caminata_model.date = date
        caminata_model.image = image
        caminata_model.place_id = place_id
        caminata_model.address = address
        caminata_model.latitude = latitude
        caminata_model.longitude = longitude
        caminata_model.user_id = user_id

        session.merge(caminata_model)
        session.commit()
        session.refresh(caminata_model)

        logger.debug("Updated: {}".format(caminata_model))
        return mapper.caminata_model_to_entity(caminata_model)

    def put_participant(self, caminata_id, user_id) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata_model: CaminataModel = session.query(CaminataModel).get(caminata_id)
        if caminata_model is None:
            return Caminata.NULL

        if user_id not in caminata_model.participants:
            participants = caminata_model.participants.copy()
            participants.append(user_id)
            caminata_model.participants = participants
        session.merge(caminata_model)
        session.commit()
        session.refresh(caminata_model)

        logger.debug("Updated: {}".format(caminata_model))
        return mapper.caminata_model_to_entity(caminata_model)

    def delete_participant(self, caminata_id, user_id) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata_model: CaminataModel = session.query(CaminataModel).get(caminata_id)
        if caminata_model is None:
            return Caminata.NULL

        if user_id in caminata_model.participants:
            participants = caminata_model.participants.copy()
            participants.remove(user_id)
            caminata_model.participants = participants
        session.merge(caminata_model)
        session.commit()
        session.refresh(caminata_model)

        logger.debug("Updated: {}".format(caminata_model))
        return mapper.caminata_model_to_entity(caminata_model)

    def delete(self, caminata_id) -> Caminata:
        session = SQLAlchemyCaminataStore.get_session()
        caminata = session.query(CaminataModel).get(caminata_id)
        if caminata:
            session.delete(caminata)
            session.commit()
            logger.debug("Deleted: {}".format(caminata))
            return mapper.caminata_model_to_entity(caminata)
        return Caminata.NULL

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyCaminataStore.dal.Session()
