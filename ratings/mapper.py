from ratings.dto import RatingDto
from ratings.entities.rating import Rating


def to_dto(rating: Rating):
    if rating is Rating.NULL:
        return RatingDto.NULL

    return RatingDto(
        rating.rating_id,
        rating.associated_id,
        rating.associated_type,
        rating.user_id,
        rating.rating_type,
        rating.date,
        rating.value
    )


def to_entity(rating_dto: RatingDto):
    return Rating(
        rating_dto.rating_id,
        rating_dto.associated_id,
        rating_dto.associated_type,
        rating_dto.user_id,
        rating_dto.rating_type,
        rating_dto.date,
        rating_dto.value
    )
