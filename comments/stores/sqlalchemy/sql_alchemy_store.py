from typing import List
import colorlog
from sqlalchemy.orm import Session

from comments.entities.comment import Comment
from comments.stores.sqlalchemy.models import CommentModel
from comments.stores.sqlalchemy import mapper
from comments.stores.sqlalchemy.data_access_layer import DataAccessLayer
from comments.stores.comment_store import CommentStore

logger = colorlog.getLogger('SQLAlchemyCommentStore')


class SQLAlchemyCommentStore(CommentStore):
    dal = None

    def __new__(cls, conn_string):
        cls.dal = DataAccessLayer(conn_string)
        cls.dal.connect()
        cls.dal.session = cls.dal.Session()
        return super().__new__(cls)

    @staticmethod
    def get_session() -> Session:
        return SQLAlchemyCommentStore.dal.Session()

    def add(self, comment_id, video_id, user_id, username, date, text, positive_votes, negative_votes, report,
            status) -> Comment:
        session = SQLAlchemyCommentStore.get_session()
        comment_model = CommentModel(id=comment_id,
                                     video_id=video_id,
                                     user_id=user_id,
                                     username=username,
                                     date=date,
                                     text=text,
                                     positive_votes=positive_votes,
                                     negative_votes=negative_votes,
                                     report=report,
                                     status=status)
        session.add(comment_model)
        session.commit()
        session.refresh(comment_model)

        logger.debug("Added: {}".format(comment_model))
        return mapper.comment_model_to_entity(comment_model)

    def get(self, comment_id) -> Comment:
        session = SQLAlchemyCommentStore.get_session()
        comment_model = session.query(CommentModel).get(comment_id)
        logger.debug("Collected: {}".format(comment_model))
        return Comment.NULL if comment_model is None else mapper.comment_model_to_entity(comment_model)

    def get_all(self) -> List[Comment]:
        session = SQLAlchemyCommentStore.get_session()
        comment_models = session.query(CommentModel)
        logger.debug("Collected all comments")
        return mapper.query_comment_model_to_entity_list(comment_models)

    def get_by_user(self, user_id) -> List[Comment]:
        session = SQLAlchemyCommentStore.get_session()
        comment_models = session.query(CommentModel).filter_by(user_id=user_id)
        logger.debug("Collected: {}".format("comments where user_id: " + str(user_id)))
        return mapper.query_comment_model_to_entity_list(comment_models)

    def get_by_video(self, video_id) -> List[Comment]:
        session = SQLAlchemyCommentStore.get_session()
        comment_models = session.query(CommentModel).filter_by(video_id=video_id)
        logger.debug("Collected: {}".format("comments where video_id: " + str(video_id)))
        return mapper.query_comment_model_to_entity_list(comment_models)

    def get_by_user_and_video(self, user_id, video_id) -> List[Comment]:
        session = SQLAlchemyCommentStore.get_session()
        comment_models = session.query(CommentModel).filter_by(user_id=user_id, video_id=video_id)
        logger.debug(
            "Collected: {} comments where user_id is {}, and video_id is {}".format(comment_models, user_id, video_id))
        return mapper.query_comment_model_to_entity_list(comment_models)

    def update(self, comment_entity) -> Comment:
        session = SQLAlchemyCommentStore.get_session()
        comment_model: CommentModel = session.query(CommentModel).get(comment_entity.comment_id)
        if comment_model is None:
            return Comment.NULL

        comment_model.comment_id = comment_entity.comment_id
        comment_model.video_id = comment_entity.video_id
        comment_model.user_id = comment_entity.user_id
        comment_model.username = comment_entity.username
        comment_model.date = comment_entity.date
        comment_model.text = comment_entity.text
        comment_model.positive_votes = comment_entity.positive_votes
        comment_model.negative_votes = comment_entity.negative_votes
        comment_model.report = comment_entity.report
        comment_model.status = comment_entity.status.value

        session.merge(comment_model)
        session.commit()
        session.refresh(comment_model)

        logger.debug("Updated: {}".format(comment_model))
        return mapper.comment_model_to_entity(comment_model)

    def delete(self, comment_id) -> Comment:
        session = SQLAlchemyCommentStore.get_session()
        comment_model = session.query(CommentModel).get(comment_id)
        if comment_model:
            session.delete(comment_model)
            session.commit()
            logger.debug("Deleted: {}".format(comment_model))
            return mapper.comment_model_to_entity(comment_model)
        return Comment.NULL
