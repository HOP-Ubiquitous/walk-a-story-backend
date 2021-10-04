import json
from utils.coordinates import Coordinates
from utils.null_object import Null


class LocationDto:
    NULL = Null()

    def __init__(self,
                 location_id,
                 is_active,
                 type,
                 subtype,
                 title,
                 description,
                 coordinates: Coordinates,
                 workers,
                 owner_user_id,
                 main_video_id,
                 creation_date):
        self.__location_id = location_id
        self.is_active = is_active
        self.type = type
        self.subtype = subtype
        self.title = title
        self.description = description
        self.coordinates = coordinates
        self.workers = workers
        self.owner_user_id = owner_user_id
        self.main_video_id = main_video_id
        self.creation_date = creation_date

    def location_id(self):
        return self.__location_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.__location_id,
            'isActive': self.is_active,
            'type': self.type,
            'subtype': self.subtype,
            'title': self.title,
            'description': self.description,
            'coordinates': self.coordinates.to_dict(),
            'workers': self.workers,
            'ownerUserId': self.owner_user_id,
            'mainVideoId': self.main_video_id,
            'creationDate': str(self.creation_date.strftime('%Y-%m-%dT%H:%M:%S')),
        }
