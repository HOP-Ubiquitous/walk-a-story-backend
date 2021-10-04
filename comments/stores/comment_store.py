from typing import List

from comments.entities.comment import Comment


class CommentStore:
    def add(self, comment_id, video_id, user_id, username, date, text, positive_votes, negative_votes, report, status) -> Comment:
        raise NotImplementedError('you must implement this method')

    def get(self, comment_id) -> Comment:
        raise NotImplementedError('you must implement this method')

    def get_all(self) -> List[Comment]:
        raise NotImplementedError('you must implement this method')

    def get_by_user(self, user_id) -> List[Comment]:
        raise NotImplementedError('you must implement this method')

    def get_by_video(self, video_id) -> List[Comment]:
        raise NotImplementedError('you must implement this method')

    def get_by_user_and_video(self, user_id, video_id) -> List[Comment]:
        raise NotImplementedError('you must implement this method')

    def update(self, comment_entity) -> Comment:
        raise NotImplementedError('you must implement this method')

    def delete(self, comment_id) -> Comment:
        raise NotImplementedError('you must implement this method')
