import colorlog

from locations.dto import LocationDto
from locations.entities.location import Location
from utils.coordinates import Coordinates

logger = colorlog.getLogger("Mapper Location")


def to_dto(location: Location):
    if location is Location.NULL:
        return LocationDto.NULL

    return LocationDto(
        location.location_id,
        location.is_active,
        location.type,
        location.subtype,
        location.title,
        location.description,
        Coordinates(location.latitude, location.longitude),
        location.workers,
        location.owner_user_id,
        location.main_video_id,
        location.creation_date)


def to_entity(location_dto: LocationDto):
    if location_dto is LocationDto.NULL:
        return Location.NULL

    return Location(
        location_dto.location_id,
        location_dto.is_active,
        location_dto.type,
        location_dto.subtype,
        location_dto.title,
        location_dto.description,
        location_dto.coordinates.latitude,
        location_dto.coordinates.longitude,
        location_dto.workers,
        location_dto.owner_user_id,
        location_dto.main_video_id,
        location_dto.creation_date
    )
