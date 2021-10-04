import colorlog

from caminatas.dto import CaminataDto
from caminatas.entities.caminata import Caminata

logger = colorlog.getLogger("Mapper Caminata")


def to_dto(caminata: Caminata):
    if caminata is Caminata.NULL:
        return CaminataDto.NULL

    return CaminataDto(
        caminata.caminata_id,
        caminata.title,
        caminata.description,
        caminata.date,
        caminata.image,
        caminata.place_id,
        caminata.address,
        caminata.latitude,
        caminata.longitude,
        caminata.user_id,
        caminata.participants)


def to_entity(caminata_dto: CaminataDto):
    if caminata_dto is CaminataDto.NULL:
        return Caminata.NULL

    return Caminata(
        caminata_dto.caminata_id(),
        caminata_dto.title,
        caminata_dto.description,
        caminata_dto.date,
        caminata_dto.image,
        caminata_dto.place_id,
        caminata_dto.address,
        caminata_dto.latitude,
        caminata_dto.longitude,
        caminata_dto.user.user_id,
        caminata_dto.participants
    )
