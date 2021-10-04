from sqlalchemy.orm import Query

from users.entities.user import User
from users.stores.sqlalchemy.models import UserModel


def user_model_to_entity(user_model: UserModel):
    return User(user_model.id, user_model.password, user_model.username, user_model.email, user_model.name,
                user_model.admin, user_model.birth_date)


def query_user_model_to_entity_list(query_user_models: Query):
    return [
        User(user_model.id, user_model.password, user_model.username, user_model.email, user_model.name,
             user_model.admin, user_model.birth_date)
        for user_model in query_user_models.all()
    ]
