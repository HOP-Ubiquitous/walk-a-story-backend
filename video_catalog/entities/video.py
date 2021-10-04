import datetime

from utils.coordinates import Coordinates
from utils.null_object import Null


class Video:
    NULL = Null()

    def __init__(self, id, g_path, public_url, analysis_url, file_public, file_status, user_id, place_id, title,
                 description, username, creation_date, latitude, longitude, positive_votes, negative_votes, reports):
        self.id = id
        self.g_path = g_path
        self.public_url = public_url
        self.file_public = file_public
        self.analysis_url = analysis_url
        self.file_status = file_status
        self.user_id = user_id
        self.place_id = place_id
        self.title = title
        self.description = description
        self.username = username
        self.creation_date: datetime = creation_date
        self.coordinates = Coordinates(latitude, longitude)
        self.positive_votes = positive_votes
        self.negative_votes = negative_votes
        self.reports = reports
