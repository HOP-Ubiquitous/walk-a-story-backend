from sqlalchemy.orm import Query

from locations.entities.location import Location
from locations.stores.sqlalchemy.models import LocationModel


def location_model_to_entity(location_model: LocationModel):
    return Location(
        location_model.id,
        location_model.is_active,
        location_model.type,
        location_model.subtype,
        location_model.title,
        location_model.description,
        location_model.latitude,
        location_model.longitude,
        location_model.workers,
        location_model.owner_user_id,
        location_model.main_video_id,
        location_model.creation_date
    )


def query_location_model_to_entity_list(query_location_models: Query):
    return [
        Location(
            location_model.id,
            location_model.is_active,
            location_model.type,
            location_model.subtype,
            location_model.title,
            location_model.description,
            location_model.latitude,
            location_model.longitude,
            location_model.workers,
            location_model.owner_user_id,
            location_model.main_video_id,
            location_model.creation_date
        )
        for location_model in query_location_models.all()
    ]


def first_query_location_model_to_entity_list(query_location_models: Query):
    if len(query_location_models.all()) != 1:
        return []
    return location_model_to_entity(query_location_models.first())
