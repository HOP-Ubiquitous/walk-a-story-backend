from sqlalchemy.orm import Query

from caminatas.entities.caminata import Caminata
from caminatas.stores.sqlalchemy.models import CaminataModel


def caminata_model_to_entity(caminata_model: CaminataModel):
    return Caminata(caminata_model.id,
                    caminata_model.title,
                    caminata_model.description,
                    caminata_model.date,
                    caminata_model.image,
                    caminata_model.place_id,
                    caminata_model.address,
                    caminata_model.latitude,
                    caminata_model.longitude,
                    caminata_model.user_id,
                    caminata_model.participants)


def query_caminata_model_to_entity_list(query_caminata_models: Query):
    return [
        Caminata(caminata_model.id,
                 caminata_model.title,
                 caminata_model.description,
                 caminata_model.date,
                 caminata_model.image,
                 caminata_model.place_id,
                 caminata_model.address,
                 caminata_model.latitude,
                 caminata_model.longitude,
                 caminata_model.user_id,
                 caminata_model.participants)
        for caminata_model in query_caminata_models.all()
    ]


def first_query_caminata_model_to_entity_list(query_caminata_models: Query):
    if len(query_caminata_models.all()) != 1:
        return []
    return caminata_model_to_entity(query_caminata_models.first())
