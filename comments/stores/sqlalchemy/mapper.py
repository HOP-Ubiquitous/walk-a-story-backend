from sqlalchemy.orm import Query

from comments.entities.comment import Comment, CommentStatus
from comments.stores.sqlalchemy.models import CommentModel


def comment_model_to_entity(comment_model: CommentModel):
    return Comment(comment_model.id,
                   comment_model.video_id,
                   comment_model.user_id,
                   comment_model.username,
                   comment_model.date,
                   comment_model.text,
                   comment_model.positive_votes,
                   comment_model.negative_votes,
                   comment_model.report,
                   CommentStatus(comment_model.status))


def query_comment_model_to_entity_list(query_comment_models: Query):
    return [
        Comment(comment_model.id,
                comment_model.video_id,
                comment_model.user_id,
                comment_model.username,
                comment_model.date,
                comment_model.text,
                comment_model.positive_votes,
                comment_model.negative_votes,
                comment_model.report,
                CommentStatus(comment_model.status))
        for comment_model in query_comment_models.all()
    ]


def first_query_comment_model_to_entity_list(query_comment_models: Query):
    if len(query_comment_models.all()) != 1:
        return []
    return comment_model_to_entity(query_comment_models.first())
