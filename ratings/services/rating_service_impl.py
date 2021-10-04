import uuid
from datetime import datetime
from http import HTTPStatus
from typing import List

import colorlog

from ratings import mapper
from ratings.dto import RatingDto, AssociatedType, RatingType
from ratings.ratings_error import RatingsError
from ratings.services.rating_service import RatingService
from ratings.stores.rating_store import RatingStore

logger = colorlog.getLogger('RatingsServiceImpl')


class RatingServiceImpl(RatingService):
    __instance = None

    def __new__(cls, rating_store, default_report_value, max_times_user_vote):
        if RatingServiceImpl.__instance is None:
            RatingServiceImpl.__instance = RatingService.__new__(cls)
        return RatingServiceImpl.__instance

    def __init__(self, rating_store, default_report_value, max_times_user_vote):
        self.rating_store: RatingStore = rating_store
        self.default_report_value = default_report_value
        self.max_times_user_vote = max_times_user_vote

    def __add_rating(self, associated_id, associated_type, user_id, rating_type, value):
        if value != 1 and value != -1:
            raise RatingsError('Rating value error, only 1 or -1', status=HTTPStatus.PRECONDITION_FAILED)
        ratings_dto = self.rating_store.get_by_associated_id_by_associated_type_by_rating_type_by_user_id(
            associated_id,
            associated_type.value,
            rating_type.value,
            user_id
        )
        used_already_voted = len(ratings_dto) >= self.max_times_user_vote
        if used_already_voted:
            raise RatingsError('User has already voted this rating', status=HTTPStatus.PRECONDITION_FAILED)
        rating_entity = self.rating_store.add(
            str(uuid.uuid4()),
            associated_id,
            associated_type.value,
            user_id,
            rating_type.value,
            datetime.now(),
            value)
        return mapper.to_dto(rating_entity)

    def get_rating_reports_by_user_id(self, user_id):
        rating_entities = self.rating_store.get_by_user_id(user_id)
        return [mapper.to_dto(rating_entity) for rating_entity in rating_entities]

    def add_rating_vote_to_comment(self, comment_id, user_id, value) -> RatingDto:
        return self.__add_rating(comment_id, AssociatedType.COMMENT, user_id, RatingType.VOTE, value)

    def add_rating_report_to_comment(self, comment_id, user_id) -> RatingDto:
        return self.__add_rating(
            comment_id,
            AssociatedType.COMMENT,
            user_id,
            RatingType.REPORT,
            self.default_report_value)

    def add_rating_vote_to_video(self, video_id, user_id, value) -> RatingDto:
        return self.__add_rating(video_id, AssociatedType.VIDEO, user_id, RatingType.VOTE, value)

    def add_rating_report_to_video(self, video_id, user_id) -> RatingDto:
        return self.__add_rating(video_id, AssociatedType.VIDEO, user_id, RatingType.REPORT, self.default_report_value)

    def get_rating_votes_to_video_comments_by_user(self, comment_id, user_id) -> List[RatingDto]:
        rating_entities = self.rating_store.get_by_associated_id_by_associated_type_by_rating_type_by_user_id(
            comment_id, AssociatedType.COMMENT.value, RatingType.VOTE.value, user_id)
        return [mapper.to_dto(rating_entity) for rating_entity in rating_entities]

    def get_rating_reports_to_video_comments_by_user(self, comment_id, user_id) -> List[RatingDto]:
        rating_entities = self.rating_store.get_by_associated_id_by_associated_type_by_rating_type_by_user_id(
            comment_id, AssociatedType.COMMENT.value, RatingType.REPORT.value, user_id)
        return [mapper.to_dto(rating_entity) for rating_entity in rating_entities]

    def get_rating_votes_to_video_by_user(self, video_id, user_id) -> List[RatingDto]:
        rating_entities = self.rating_store.get_by_associated_id_by_associated_type_by_rating_type_by_user_id(
            video_id, AssociatedType.VIDEO.value, RatingType.VOTE.value, user_id)
        return [mapper.to_dto(rating_entity) for rating_entity in rating_entities]

    def get_rating_reports_to_video_by_user(self, video_id, user_id) -> List[RatingDto]:
        rating_entities = self.rating_store.get_by_associated_id_by_associated_type_by_rating_type_by_user_id(
            video_id, AssociatedType.VIDEO.value, RatingType.REPORT.value, user_id)
        return [mapper.to_dto(rating_entity) for rating_entity in rating_entities]

    def delete_rating(self, rating_id) -> List[RatingDto]:
        raise RatingsError('Not implemented', status=HTTPStatus.NOT_IMPLEMENTED)
        rating_entity = self.rating_store.delete(rating_id)
        return mapper.to_dto(rating_entity)
