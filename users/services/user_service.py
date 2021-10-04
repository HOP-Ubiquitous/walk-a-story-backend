from typing import List

from users.dto import UserDto


class UserService:
    def register_user(self, username, password, email, name, admin, birth_date)-> UserDto:
        raise NotImplementedError('you must implement this method')

    def login_user(self, username, password) -> UserDto:
        raise NotImplementedError('you must implement this method')

    def get_all_users(self) -> List[UserDto]:
        raise NotImplementedError('you must implement this method')

    def get_user_by_id(self, user_id) -> UserDto:
        raise NotImplementedError('you must implement this method')

    def get_user_by_username(self, username) -> UserDto:
        raise NotImplementedError('you must implement this method')

    def update_user(self, user_id, password, username, email, name, admin, birth_date) -> UserDto:
        raise NotImplementedError('you must implement this method')

    def update_role_user(self, user_id, is_admin):
        raise NotImplementedError('you must implement this method')

    def update_role_admin(self, user_id, is_admin):
        raise NotImplementedError('you must implement this method')

    def delete_user(self, user_id) -> UserDto:
        raise NotImplementedError('you must implement this method')

    def delete_admin(self, user_id) -> UserDto:
        raise NotImplementedError('you must implement this method')
