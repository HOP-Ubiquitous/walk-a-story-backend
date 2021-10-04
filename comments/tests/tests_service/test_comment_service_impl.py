import datetime
import unittest
from unittest.mock import Mock

import colorlog

from comments.dto import CommentDto, CommentDtoStatus
from comments.entities.comment import Comment, CommentStatus
from comments.services.comment_service_impl import CommentServiceImpl
from comments.stores.comment_store import CommentStore

logger = colorlog.getLogger('TestCommentServiceImpl')


class TestCommentServiceImpl(unittest.TestCase):

    def setUp(self):
        self.comment_store = CommentStore()
        self.max_comments_by_user = 1
        self.comment_service = CommentServiceImpl(self.comment_store, self.max_comments_by_user)
        self.test_comment_entity = Comment(
            'entity_id',
            'video_id',
            'user_id',
            'username',
            datetime.date.today(),
            'text',
            0,
            0,
            0,
            CommentStatus.ENABLED
        )
        self.test_comment_dto = CommentDto(
            'entity_id',
            'video_id',
            'user_id',
            'username',
            datetime.date.today(),
            'text',
            0,
            0,
            0,
            CommentDtoStatus.ENABLED
        )

    def test_get_comment_null_by_comment_id_return_comment_dto_null(self):
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = Comment.NULL

        comment_dto = self.comment_service.get_comment('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_get_comment_by_comment_id_return_comment_dto(self):
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.get_comment('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_get_all_comments_empty_return_empty_comment_dto_list(self):
        self.comment_store.get_all = Mock()
        self.comment_store.get_all.return_value = []

        comment_dto_list = self.comment_service.get_all_comments()
        self.assertEqual([], comment_dto_list)

    def test_get_all_comments_return_comment_dto_list(self):
        self.comment_store.get_all = Mock()
        self.comment_store.get_all.return_value = [self.test_comment_entity]

        comment_dto_list = self.comment_service.get_all_comments()
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto_list[0].to_dict())

    def test_get_comments_by_not_user_id_return_empty_comment_dto_list(self):
        self.comment_store.get_by_user = Mock()
        self.comment_store.get_by_user.return_value = []

        comment_dto_list = self.comment_service.get_comments_by_user('not_user_id')
        self.assertEqual([], comment_dto_list)

    def test_get_comments_by_user_id_return_empty_comment_dto_list(self):
        self.comment_store.get_by_user = Mock()
        self.comment_store.get_by_user.return_value = [self.test_comment_entity]

        comment_dto_list = self.comment_service.get_comments_by_user('user_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto_list[0].to_dict())

    def test_get_comments_by_not_video_id_return_empty_comment_dto_list(self):
        self.comment_store.get_by_video = Mock()
        self.comment_store.get_by_video.return_value = []

        comment_dto_list = self.comment_service.get_comments_by_video('not_video_id')
        self.assertEqual([], comment_dto_list)

    def test_get_comments_by_video_id_return_empty_comment_dto_list(self):
        self.comment_store.get_by_video = Mock()
        self.comment_store.get_by_video.return_value = [self.test_comment_entity]

        comment_dto_list = self.comment_service.get_comments_by_video('video_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto_list[0].to_dict())

    def test_get_comments_by_not_user_id_video_id_return_empty_comment_dto_list(self):
        self.comment_store.get_by_user_and_video = Mock()
        self.comment_store.get_by_user_and_video.return_value = []

        comment_dto_list = self.comment_service.get_comments_by_user_and_video('not_user_id', 'not_video_id', )
        self.assertEqual([], comment_dto_list)

    def test_get_comments_by_user_id_video_id_return_empty_comment_list(self):
        self.comment_store.get_by_user_and_video = Mock()
        self.comment_store.get_by_user_and_video.return_value = [self.test_comment_entity]

        comment_dto_list = self.comment_service.get_comments_by_user_and_video('user_id', 'video_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto_list[0].to_dict())

    def test_enable_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.update.return_value = Comment.NULL
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.enable_comment('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_enable_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity
        updated_comment_entity = self.test_comment_entity
        updated_comment_entity.status = CommentStatus.ENABLED

        self.comment_store.update.return_value = updated_comment_entity

        comment_dto = self.comment_service.enable_comment('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_disable_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.update.return_value = Comment.NULL
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.disable_comment('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_disable_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity
        updated_comment_entity = self.test_comment_entity
        updated_comment_entity.status = CommentStatus.ENABLED

        self.comment_store.update.return_value = updated_comment_entity

        comment_dto = self.comment_service.disable_comment('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_add_positive_vote_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.update.return_value = Comment.NULL
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.add_positive_vote('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_add_positive_vote_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity
        updated_comment_entity = self.test_comment_entity
        updated_comment_entity.status = CommentStatus.ENABLED

        self.comment_store.update.return_value = updated_comment_entity

        comment_dto = self.comment_service.add_positive_vote('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_add_negative_vote_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.update.return_value = Comment.NULL
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.add_negative_vote('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_add_negative_vote_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity
        updated_comment_entity = self.test_comment_entity
        updated_comment_entity.status = CommentStatus.ENABLED

        self.comment_store.update.return_value = updated_comment_entity

        comment_dto = self.comment_service.add_negative_vote('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_add_report_vote_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.update.return_value = Comment.NULL
        self.comment_store.get.return_value = self.test_comment_entity

        comment_dto = self.comment_service.add_report('undefined_id')
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_add_report_vote_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.get = Mock()
        self.comment_store.get.return_value = self.test_comment_entity
        updated_comment_entity = self.test_comment_entity
        updated_comment_entity.status = CommentStatus.ENABLED

        self.comment_store.update.return_value = updated_comment_entity

        comment_dto = self.comment_service.add_report('entity_id')
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_update_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.update = Mock()
        self.comment_store.update.return_value = Comment.NULL

        comment_dto = self.comment_service.update_comment(CommentDto.NULL)
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_update_comment_comment_id_return_comment_dto(self):
        self.comment_store.update = Mock()
        self.comment_store.update.return_value = self.test_comment_entity

        comment_dto = self.comment_service.update_comment(self.test_comment_dto)
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())

    def test_delete_comment_not_comment_id_return_comment_dto_null(self):
        self.comment_store.delete = Mock()
        self.comment_store.delete.return_value = Comment.NULL

        comment_dto = self.comment_service.delete_comment(CommentDto.NULL)
        self.assertEqual(CommentDto.NULL, comment_dto)

    def test_delete_comment_comment_id_return_comment_dto(self):
        self.comment_store.delete = Mock()
        self.comment_store.delete.return_value = self.test_comment_entity

        comment_dto = self.comment_service.delete_comment(self.test_comment_dto)
        self.assertEqual(self.test_comment_dto.to_dict(), comment_dto.to_dict())