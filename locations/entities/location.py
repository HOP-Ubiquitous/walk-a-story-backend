from datetime import datetime
from utils.null_object import Null


class Location:
    NULL = Null()

    def __init__(self,
                 location_id,
                 is_active,
                 type,
                 subtype,
                 title,
                 description,
                 latitude,
                 longitude,
                 workers,
                 owner_user_id,
                 main_video_id,
                 creation_date=datetime.utcnow()):
        self.location_id = location_id
        self.is_active = is_active
        self.type = type
        self.subtype = subtype
        self.title = title
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.workers = workers
        self.owner_user_id = owner_user_id
        self.main_video_id = main_video_id
        self.creation_date = creation_date
