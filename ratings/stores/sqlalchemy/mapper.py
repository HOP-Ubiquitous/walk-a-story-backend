from sqlalchemy.orm import Query

from ratings.entities.rating import Rating
from ratings.stores.sqlalchemy.models import RatingModel


def rating_model_to_entity(rating_model: RatingModel):
    return Rating(
        rating_model.id,
        rating_model.associated_id,
        rating_model.associated_type,
        rating_model.user_id,
        rating_model.rating_type,
        rating_model.date,
        rating_model.value
    )


def query_rating_model_to_entity_list(query_rating_models: Query):
    return [
        Rating(
            rating_model.id,
            rating_model.associated_id,
            rating_model.associated_type,
            rating_model.user_id,
            rating_model.rating_type,
            rating_model.date,
            rating_model.value
        )
        for rating_model in query_rating_models.all()
    ]


def first_query_rating_model_to_entity_list(query_rating_models: Query):
    if len(query_rating_models.all()) != 1:
        return Rating.NULL
    return rating_model_to_entity(query_rating_models.first())
