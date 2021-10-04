from typing import List

from ratings.dto import RatingDto


class RatingService:

    def get_rating_reports_by_user_id(self, user_id):
        raise NotImplementedError('you must implement this method')

    def add_rating_vote_to_comment(self, comment_id, user_id, value) -> RatingDto:
        raise NotImplementedError('you must implement this method')

    def add_rating_report_to_comment(self, comment_id, user_id) -> RatingDto:
        raise NotImplementedError('you must implement this method')

    def add_rating_vote_to_video(self, video_id, user_id, value) -> RatingDto:
        raise NotImplementedError('you must implement this method')

    def add_rating_report_to_video(self, video_id, user_id) -> RatingDto:
        raise NotImplementedError('you must implement this method')

    def get_rating_votes_to_video_comments_by_user(self, video_id, user_id) -> List[RatingDto]:
        raise NotImplementedError('you must implement this method')

    def get_rating_reports_to_video_comments_by_user(self, video_id, user_id) -> List[RatingDto]:
        raise NotImplementedError('you must implement this method')

    def get_rating_votes_to_video_by_user(self, video_id, user_id) -> List[RatingDto]:
        raise NotImplementedError('you must implement this method')

    def get_rating_reports_to_video_by_user(self, video_id, user_id) -> List[RatingDto]:
        raise NotImplementedError('you must implement this method')

    def delete_rating(self, rating_id) -> RatingDto:
        raise NotImplementedError('you must implement this method')
