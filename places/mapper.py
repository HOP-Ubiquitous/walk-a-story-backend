import colorlog

from places.dto import PointOfInterestDto, CityDto
from places.entities.city import City
from places.entities.point_of_interest import PointOfInterest

logger = colorlog.getLogger("Mapper Places")


def point_of_interest_to_dto(point_of_interest: PointOfInterest):
    if point_of_interest is PointOfInterest.NULL:
        return PointOfInterestDto.NULL

    return PointOfInterestDto(
        point_of_interest.id,
        point_of_interest.name,
        point_of_interest.city_id,
        point_of_interest.latitude,
        point_of_interest.longitude
    )


def point_of_interest_to_entity(point_of_interest_dto: PointOfInterestDto):
    if point_of_interest_dto is PointOfInterestDto.NULL:
        return PointOfInterest.NULL

    return PointOfInterest(
        point_of_interest_dto.id,
        point_of_interest_dto.name,
        point_of_interest_dto.city_id,
        point_of_interest_dto.latitude,
        point_of_interest_dto.longitude
    )


def city_to_dto(city: City):
    if city is City.NULL:
        return CityDto.NULL

    points_of_interest_dto = []
    for point_of_interest in city.points_of_interest:
        points_of_interest_dto.append(point_of_interest_to_dto(point_of_interest))

    return CityDto(
        city.id,
        city.name,
        points_of_interest_dto
    )


def city_to_entity(city_dto: CityDto):
    if city_dto is CityDto.NULL:
        return City.NULL

    points_of_interest_entity = []
    for point_of_interest in city_dto.points_of_interest:
        points_of_interest_entity.append(point_of_interest_to_dto(point_of_interest))

    return City(
        city_dto.id,
        city_dto.name,
        points_of_interest_entity
    )
