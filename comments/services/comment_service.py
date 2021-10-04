from typing import List

from comments.dto import CommentDto


class CommentService:
    def add_comment(self, video_id, user_id, username, date, text, status) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def get_comment(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def get_all_comments(self) -> List[CommentDto]:
        raise NotImplementedError('you must implement this method')

    def get_comments_by_user(self, user_id) -> List[CommentDto]:
        raise NotImplementedError('you must implement this method')

    def get_comments_by_video(self, video_id) -> List[CommentDto]:
        raise NotImplementedError('you must implement this method')

    def get_comments_by_user_and_video(self, user_id, video_id) -> List[CommentDto]:
        raise NotImplementedError('you must implement this method')

    def enable_comment(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def disable_comment(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def add_positive_vote(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def add_negative_vote(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def add_report(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def update_comment(self, comment_dto) -> CommentDto:
        raise NotImplementedError('you must implement this method')

    def delete_comment(self, comment_id) -> CommentDto:
        raise NotImplementedError('you must implement this method')
