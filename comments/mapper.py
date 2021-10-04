import colorlog

from comments.dto import CommentDto, CommentDtoStatus
from comments.entities.comment import Comment, CommentStatus

logger = colorlog.getLogger("Mapper Comment")


def to_dto(comment: Comment):
    if comment is Comment.NULL:
        return CommentDto.NULL

    return CommentDto(
        comment.comment_id,
        comment.video_id,
        comment.user_id,
        comment.username,
        comment.date,
        comment.text,
        comment.positive_votes,
        comment.negative_votes,
        comment.report,
        CommentDtoStatus(comment.status.value))


def to_entity(comment_dto: CommentDto):
    if comment_dto is Comment.NULL:
        return Comment.NULL

    return Comment(
        comment_dto.comment_id,
        comment_dto.video_id,
        comment_dto.user_id,
        comment_dto.username,
        comment_dto.date,
        comment_dto.text,
        comment_dto.positive_votes,
        comment_dto.negative_votes,
        comment_dto.report,
        CommentStatus(comment_dto.status.value))
