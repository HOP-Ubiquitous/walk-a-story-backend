import uuid
from typing import List
from dateutil.parser import parse
from comments import mapper
from comments.services.comment_service import CommentService
from comments.stores.comment_store import CommentStore
from comments.dto import CommentDto
from comments.entities.comment import CommentStatus

DEFAULT_RATING_VALUE = 0


class CommentServiceImpl(CommentService):

    def __init__(self, comment_store: CommentStore, max_comments_by_user):
        self.comment_store = comment_store
        self.max_comments_by_user = max_comments_by_user

    def add_comment(self, video_id, user_id, username, date, text, status) -> CommentDto:
        comments_entity = self.comment_store.get_by_user_and_video(user_id, video_id)
        user_already_commented = len(comments_entity) >= self.max_comments_by_user
        if user_already_commented:
            return CommentDto.NULL
        comment_entity = self.comment_store.add(
            str(uuid.uuid4()),
            video_id,
            user_id,
            username,
            parse(date),
            text,
            DEFAULT_RATING_VALUE,
            DEFAULT_RATING_VALUE,
            DEFAULT_RATING_VALUE,
            status
        )
        return mapper.to_dto(comment_entity)

    def get_comment(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        return mapper.to_dto(comment_entity)

    def get_all_comments(self) -> List[CommentDto]:
        comments_entities = self.comment_store.get_all()
        return [mapper.to_dto(comment_entity) for comment_entity in comments_entities]

    def get_comments_by_user(self, user_id) -> List[CommentDto]:
        comments_entities = self.comment_store.get_by_user(user_id)
        return [mapper.to_dto(comment_entity) for comment_entity in comments_entities]

    def get_comments_by_video(self, video_id) -> List[CommentDto]:
        comments_entities = self.comment_store.get_by_video(video_id)
        return [mapper.to_dto(comment_entity) for comment_entity in comments_entities]

    def get_comments_by_user_and_video(self, user_id, video_id) -> List[CommentDto]:
        comments_entities = self.comment_store.get_by_user_and_video(user_id, video_id)
        return [mapper.to_dto(comment_entity) for comment_entity in comments_entities]

    def enable_comment(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        comment_dto = mapper.to_dto(comment_entity)
        comment_dto.status = CommentStatus.ENABLED
        comment_entity_updated = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity_updated)

    def disable_comment(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        comment_dto = mapper.to_dto(comment_entity)
        comment_dto.status = CommentStatus.DISABLED
        comment_entity_updated = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity_updated)

    def add_positive_vote(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        comment_dto = mapper.to_dto(comment_entity)
        comment_dto.positive_votes += 1
        comment_entity_updated = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity_updated)

    def add_negative_vote(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        comment_dto = mapper.to_dto(comment_entity)
        comment_dto.negative_votes += 1
        comment_entity_updated = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity_updated)

    def add_report(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.get(comment_id)
        comment_dto = mapper.to_dto(comment_entity)
        comment_dto.report += 1
        comment_entity_updated = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity_updated)

    def update_comment(self, comment_dto) -> CommentDto:
        comment_entity = self.comment_store.update(mapper.to_entity(comment_dto))
        return mapper.to_dto(comment_entity)

    def delete_comment(self, comment_id) -> CommentDto:
        comment_entity = self.comment_store.delete(comment_id)
        return mapper.to_dto(comment_entity)
