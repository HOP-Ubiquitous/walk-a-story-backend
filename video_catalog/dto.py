import json
from enum import Enum

from utils.coordinates import Coordinates
from utils.null_object import Null


class FileStatus(Enum):
    VALID = 0
    INVALID = 1
    HUMAN_REQUIRED = 2
    ANALYZING = 3
    UPLOADED = 4
    FORMAT_ERROR = 5
    DELETED = 6


class VideoDto:
    NULL = Null()

    def __init__(self, id, g_path, public_url, analysis_url, file_public, file_status, user_id, place_id, title,
                 description, username, creation_date, coordinates, positive_votes, negative_votes, reports):
        self.id = id
        self.g_path = g_path
        self.public_url = public_url
        self.analysis_url = analysis_url
        self.file_public = file_public
        self.file_status = file_status
        self.user_id = user_id
        self.place_id = place_id
        self.title = title
        self.description = description
        self.username = username
        self.creation_date = creation_date
        self.coordinates: Coordinates = coordinates
        self.positive_votes = positive_votes
        self.negative_votes = negative_votes
        self.reports = reports

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'id': self.id,
                'g_path': self.g_path,
                'public_url': self.public_url,
                'analysis_url': self.analysis_url,
                'file_public': self.file_public,
                'file_status': self.file_status,
                'user_id': self.user_id,
                'place_id': self.place_id,
                'title': self.title,
                'description': self.description,
                'username': self.username,
                'creation_date': str(self.creation_date),
                'coordinates': self.coordinates.to_dict(),
                'positive_votes': self.positive_votes,
                'negative_votes': self.negative_votes,
                'reports': self.reports}
