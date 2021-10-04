from enum import Enum

from utils.null_object import Null


class CommentStatus(Enum):
    ENABLED = 0
    DISABLED = 1


class Comment:
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
        self.status: CommentStatus = status
