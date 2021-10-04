from sqlalchemy.orm import Query

from places.entities.city import City
from places.entities.point_of_interest import PointOfInterest
from places.stores.sqlalchemy.models import CityModel, PointOfInterestModel


def point_of_interest_model_to_entity(point_of_interest_model: PointOfInterestModel):
    return PointOfInterest(
        point_of_interest_model.id,
        point_of_interest_model.name,
        point_of_interest_model.city_id,
        point_of_interest_model.latitude,
        point_of_interest_model.longitude
    )


def query_point_of_interest_model_to_entity_list(query_point_of_interest_model: Query):
    return [
        PointOfInterest(
            point_of_interest_model.id,
            point_of_interest_model.name,
            point_of_interest_model.city_id,
            point_of_interest_model.latitude,
            point_of_interest_model.longitude
        )
        for point_of_interest_model in query_point_of_interest_model.all()
    ]


def first_query_point_of_interest_model_to_entity_list(query_point_of_interest_model: Query):
    if len(query_point_of_interest_model.all()) != 1:
        return []
    return point_of_interest_model_to_entity(query_point_of_interest_model.first())


def city_model_to_entity(city_model: CityModel):
    entity_points_of_interest = []
    for point_of_interest in city_model.points_of_interest:
        entity_points_of_interest.append(point_of_interest_model_to_entity(point_of_interest))
    return City(
        city_model.id,
        city_model.name,
        entity_points_of_interest
    )


def query_city_model_to_entity_list(query_city_models: Query):
    return [
        city_model_to_entity(city_model)
        for city_model in query_city_models.all()
    ]


def first_query_city_model_to_entity_list(query_city_model: Query):
    if len(query_city_model.all()) != 1:
        return []
    return city_model_to_entity(query_city_model.first())
