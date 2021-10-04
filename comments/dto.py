import json
from enum import Enum

from utils.null_object import Null


class CommentDtoStatus(Enum):
    ENABLED = 0
    DISABLED = 1


class CommentDto:
    NULL = Null()

    def __init__(self, comment_id, video_id, user_id, username, date, text, positive_votes, negative_votes, report,
                 status):
        self.comment_id = comment_id
        self.video_id = video_id
        self.user_id = user_id
        self.username = username
        self.date = date
        self.text = text
        self.positive_votes = positive_votes
        self.negative_votes = negative_votes
        self.report = report
        self.status: CommentDtoStatus = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'video_id': self.video_id,
            'user_id': self.user_id,
            'username': self.username,
            'date': str(self.date.strftime('%Y-%m-%dT%H:%M:%S')),
            'text': self.text,
            'positive_votes': self.positive_votes,
            'negative_votes': self.negative_votes,
            'report': self.report,
            'status': self.status.value
        }
