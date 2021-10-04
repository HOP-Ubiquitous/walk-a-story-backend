from typing import List

import colorlog
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from users.stores.sqlalchemy import mapper
from users.entities.user import User
from users.stores.sqlalchemy.data_access_layer import DataAccessLayer
from users.stores.sqlalchemy.models import UserModel
from users.stores.user_store import UserStore

logger = colorlog.getLogger('SQLAlchemyUserStore')


class SQLAlchemyUserStore(UserStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()

        return super().__new__(cls)

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyUserStore.dal.Session()

    @staticmethod
    def exists(username):
        session = SQLAlchemyUserStore.get_session()
        users_model = session.query(UserModel).filter_by(username=username)
        if len(users_model.all()) < 1:
            return False
        else:
            return True

    def add(self, user_id, password, username, email, name, admin, birth_date) -> User:
        logger.debug("User add: " + str(user_id))
        session = SQLAlchemyUserStore.get_session()
        if self.exists(username):
            logger.error("Username exists {}".format(username))
            return User.NULL

        user_model = UserModel(id=user_id, password=generate_password_hash(password, method='sha256'),
                               username=username, email=email, name=name, admin=admin, birth_date=birth_date)

        session.add(user_model)
        session.commit()
        session.refresh(user_model)

        logger.debug("Added user: {}".format(user_model))
        user = mapper.user_model_to_entity(user_model)

        return user

    def get_user_by_id(self, user_id) -> User:
        session = SQLAlchemyUserStore.get_session()
        user_model = session.query(UserModel).get(user_id)
        logger.debug("Getting user by username: {}".format(user_id))
        # if not check_password_hash(user_model.password, password):
        #     return User.NULL

        logger.debug("Collected user: {}".format(user_model))

        return User.NULL if user_model is None else mapper.user_model_to_entity(user_model)

    def get_user_by_username_password(self, username, password) -> User:
        session = SQLAlchemyUserStore.get_session()
        users_model = session.query(UserModel).filter_by(username=username)
        logger.debug("Getting user: {}".format(username))
        if len(users_model.all()) != 1:
            return User.NULL

        user_model = users_model.first()
        if not check_password_hash(user_model.password, password):
            return User.NULL
        logger.debug("Collected user : {}".format(user_model))

        return User.NULL if user_model is None else mapper.user_model_to_entity(user_model)

    def get_user_by_id_with_no_password(self, user_id) -> User:
        session = SQLAlchemyUserStore.get_session()
        user_model = session.query(UserModel).get(user_id)
        logger.debug("Collected user : {}".format(user_model))

        return User.NULL if user_model is None else mapper.user_model_to_entity(user_model)

    def get_user_by_username(self, username) -> User:
        session = SQLAlchemyUserStore.get_session()
        users_model = session.query(UserModel).filter_by(username=username)
        logger.debug("Getting user: {}".format(username))
        if len(users_model.all()) != 1:
            return User.NULL

        user_model = users_model.first()
        logger.debug("Collected user : {}".format(user_model))

        return User.NULL if user_model is None else mapper.user_model_to_entity(user_model)

    def get_all(self) -> List[User]:
        session = SQLAlchemyUserStore.get_session()
        users = session.query(UserModel)

        logger.debug("Get all users")

        return mapper.query_user_model_to_entity_list(users)

    def update(self, user_id, password, username, email, name, admin, birth_date) -> User:
        session = SQLAlchemyUserStore.get_session()
        user_model = session.query(UserModel).get(user_id)
        logger.debug("Updating user_id: {}".format(user_id))
        if user_model is None:
            return User.NULL
        if not check_password_hash(user_model.password, password):
            return User.NULL

        user_model.password = generate_password_hash(password, method='sha256')
        user_model.username = username
        user_model.email = email
        user_model.name = name
        user_model.admin = admin
        user_model.birth_date = birth_date

        session.merge(user_model)
        session.commit()
        session.refresh(user_model)

        logger.debug("Updated user: {}".format(user_model))
        video = mapper.user_model_to_entity(user_model)
        return video

    def update_admin(self, user_id, is_admin) -> User:
        session = SQLAlchemyUserStore.get_session()
        user_model = session.query(UserModel).get(user_id)
        logger.debug("Updating user_id: {}".format(user_id))
        if user_model is None:
            return User.NULL

        user_model.admin = is_admin

        session.merge(user_model)
        session.commit()
        session.refresh(user_model)

        logger.debug("Updated user: {}".format(user_model))
        video = mapper.user_model_to_entity(user_model)
        return video

    def delete(self, user_id, password) -> User:
        session = SQLAlchemyUserStore.get_session()
        logger.debug("Deleting user: {}".format(user_id))

        user_model = session.query(UserModel).get(user_id)
        if user_model is not None:
            if not check_password_hash(user_model.password, password):
                return User.NULL

            if user_model:
                session.delete(user_model)
                session.commit()

                logger.debug("Deleted user: {}".format(user_model))
                return mapper.user_model_to_entity(user_model)

        return User.NULL

    def delete_by_admin(self, user_id) -> User:
        session = SQLAlchemyUserStore.get_session()
        logger.debug("Deleting user by admin: {}".format(user_id))

        user_model = session.query(UserModel).get(user_id)
        if user_model is None:
            return User.NULL

        session.delete(user_model)
        session.commit()

        logger.debug("Deleted user by admin: {}".format(user_model))
        return mapper.user_model_to_entity(user_model)
