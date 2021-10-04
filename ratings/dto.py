import json
from enum import Enum
from utils.null_object import Null


class RatingType(Enum):
    VOTE = 'vote'
    REPORT = 'report'


class AssociatedType(Enum):
    COMMENT = 'comment'
    VIDEO = 'video'


class RatingDto:
    NULL = Null()

    def __init__(self, rating_id, associated_id, associated_type, user_id, rating_type, date, value):
        self.rating_id = rating_id
        self.associated_id = associated_id
        self.associated_type = associated_type
        self.user_id = user_id
        self.rating_type = rating_type
        self.date = date
        self.value = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        rating_dto = {
            'rating_id': self.rating_id,
            'user_id': self.user_id
        }
        if self.rating_type == RatingType.VOTE.value:
            rating_dto.update({'value': self.value})

        if self.associated_type == AssociatedType.COMMENT.value:
            rating_dto.update({'comment_id': self.associated_id})
            return rating_dto
        elif self.associated_type == AssociatedType.VIDEO.value:
            rating_dto.update({'video_id': self.associated_id})
            return rating_dto
        else:
            rating_dto.update({'associated_id': self.associated_id})
            return rating_dto
