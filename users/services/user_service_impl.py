import datetime
import uuid
import colorlog
from typing import List

from users import mapper
from users.dto import UserDto
from users.entities.user import User
from users.services.user_service import UserService
from users.stores.user_store import UserStore
from dateutil.parser import parse

logger = colorlog.getLogger('UserServiceImpl')


class UserServiceImpl(UserService):
    def __init__(self, user_store: UserStore, super_admin_username):
        self.user_store = user_store
        self.super_admin_username = super_admin_username
        admin_dto = self.user_store.add(
            str(uuid.uuid4()),
            'password',
            'admin',
            'admin@localhost',
            'CoCrew Admin',
            True,
            parse('1990-03-18T09:00:00')
        )
        if admin_dto is UserDto.NULL:
            logger.warning('User user already exists on DB')

        user_dto = self.user_store.add(
            str(uuid.uuid4()),
            'password',
            'user',
            'user@hopu.eu',
            'Hopu User',
            False,
            parse('1990-03-18T09:00:00')
        )
        if user_dto is UserDto.NULL:
            logger.warning('User user already exists on DB')

    def register_user(self, username, password, email, name, admin, birth_date) -> UserDto:
        user_info = self.user_store.add(
            str(uuid.uuid4()),
            password,
            username,
            email,
            name,
            admin,
            parse(birth_date)
        )

        return mapper.to_dto(user_info)

    def get_user_by_id(self, user_id) -> UserDto:
        user_info = self.user_store.get_user_by_id_with_no_password(user_id)
        return mapper.to_dto(user_info)

    def login_user(self, username, password) -> UserDto:
        user_info = self.user_store.get_user_by_username_password(username, password)
        return mapper.to_dto(user_info)

    def get_all_users(self) -> List[UserDto]:
        users_info = self.user_store.get_all()
        return [mapper.to_dto(user_info) for user_info in users_info]

    def get_user_by_username(self, username) -> UserDto:
        user_info = self.user_store.get_user_by_username(username)
        return mapper.to_dto(user_info)

    def update_user(self, user_id, password, username, email, name, admin, birth_date) -> UserDto:
        user_info = self.user_store.update(user_id, password, username, email, name, admin, birth_date)
        return mapper.to_dto(user_info)

    def update_role_user(self, user_id, is_admin):
        user_info = self.user_store.get_user_by_id(user_id)
        if user_info is User.NULL or user_info.admin:
            return UserDto.NULL

        user_updated = self.user_store.update_admin(user_id, is_admin)
        return mapper.to_dto(user_updated)

    def update_role_admin(self, user_id, is_admin):
        user_updated = self.user_store.update_admin(user_id, is_admin)
        return mapper.to_dto(user_updated)

    def delete_user(self, user_id) -> UserDto:
        user_info = self.user_store.get_user_by_id(user_id)
        if user_info is User.NULL or user_info.admin:
            return UserDto.NULL
        user_removed = self.user_store.delete_by_admin(user_info.id)
        return mapper.to_dto(user_removed)

    def delete_admin(self, user_id) -> UserDto:
        user_info = self.user_store.delete_by_admin(user_id)
        if user_info is User.NULL or user_info.username == self.super_admin_username:
            return UserDto.NULL
        return mapper.to_dto(user_info)
