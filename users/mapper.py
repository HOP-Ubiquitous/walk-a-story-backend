import colorlog

from users.dto import UserDto
from users.entities.user import User

logger = colorlog.getLogger("Mapper User")


def to_dto(user: User):
    if user is User.NULL:
        return UserDto.NULL
    return UserDto(user.id, user.username, user.email, user.name, user.admin, user.birth_date)
