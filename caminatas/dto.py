import json
from datetime import datetime

from utils.null_object import Null


class CaminataDto:
    NULL = Null()

    def __init__(self, caminata_id, title, description, date, image, place_id, address, latitude, longitude, user_id,
                 participants):
        self.__caminata_id = caminata_id
        self.title = title
        self.description = description
        self.date: datetime = date
        self.image = image
        self.place_id = place_id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.user = user_id
        self.participants = participants

    def caminata_id(self):
        return self.__caminata_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        try:
            user = self.user.to_dict()
        except Exception:
            user = self.user
        return {
            'caminata_id': self.__caminata_id,
            'title': self.title,
            'description': self.description,
            'date': str(self.date.strftime('%Y-%m-%dT%H:%M:%S')),
            'image': self.image,
            'place_id': self.place_id,
            'address': self.address,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'user': user,
            'participants': self.participants
        }
