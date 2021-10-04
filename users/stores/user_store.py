from typing import List

from users.entities.user import User


class UserStore:
    def add(self, user_id, password, username, email, name, admin, birth_date) -> User:
        raise NotImplementedError('you must implement this method')

    def get_user_by_id(self, user_id) -> User:
        raise NotImplementedError('you must implement this method')

    def get_user_by_username_password(self, username, password) -> User:
        raise NotImplementedError('you must implement this method')

    def get_user_by_id_with_no_password(self, user_id) -> User:
        raise NotImplementedError('you must implement this method')

    def get_user_by_username(self, username) -> User:
        raise NotImplementedError('you must implement this method')

    def update(self, user_id, password, username, email, name, admin, birth_date) -> User:
        raise NotImplementedError('you must implement this method')

    def update_admin(self, user_id, is_admin) -> User:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[User]:
        raise NotImplementedError('you must implement this method')

    def delete(self, user_id, password) -> User:
        raise NotImplementedError('you must implement this method')

    def delete_by_admin(self, user_id) -> User:
        raise NotImplementedError('you must implement this method')
