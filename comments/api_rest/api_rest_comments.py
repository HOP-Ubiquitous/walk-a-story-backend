from http import HTTPStatus

import colorlog
import json
from flask import request, Blueprint, Flask

from comments.comments_error import CommentsError
from comments.dto import CommentDto
from comments.services.comment_service import CommentService
from users.role_required_decorators import login_required, admin_required

logger = colorlog.getLogger('REST API Comments')
comment_service: CommentService
comments = Blueprint('comments', __name__)


@comments.route('', methods=['POST'])
@comments.route('/', methods=['POST'])
@login_required
def add_comment():
    try:
        data = json.loads(request.data)
        video_id = data['video_id']
        user_id = data['user_id']
        username = data['username']
        date = data['date']
        text = data['text']
        status = 0

        comment_dto: CommentDto = comment_service.add_comment(video_id,
                                                              user_id,
                                                              username,
                                                              date,
                                                              text,
                                                              status)
        if comment_dto is CommentDto.NULL:
            raise CommentsError("comment was not created", status=HTTPStatus.BAD_REQUEST)
        else:
            message = comment_dto.to_dict()
            status = HTTPStatus.CREATED
    except CommentsError as comments_error:
        message = {"error": str(comments_error)}
        status = comments_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception add_rating_vote_to_comment: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@comments.route('', methods=['GET'])
@comments.route('/', methods=['GET'])
def get_all_comments():
    comments_dto = comment_service.get_all_comments()
    comments_list = []
    for comment_dto in comments_dto:
        comments_list.append(comment_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(comments_list),
        status=status,
        mimetype='application/json'
    )


@comments.route('/video/<video_id>', methods=['GET'])
def get_comments_by_video_id(video_id):
    comments_dto = comment_service.get_comments_by_video(video_id)
    comments_list = []
    for comment_dto in comments_dto:
        comments_list.append(comment_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(comments_list),
        status=status,
        mimetype='application/json'
    )


@comments.route('/<comment_id>/enable', methods=['PUT'])
@admin_required
def put_comment_enabled(comment_id):
    try:
        comment_dto = comment_service.enable_comment(comment_id)
        if comment_dto is CommentDto.NULL:
            raise CommentsError("comment was not enabled", status=HTTPStatus.BAD_REQUEST)
        else:
            message = {}
            status = HTTPStatus.NO_CONTENT
    except CommentsError as comments_error:
        message = {"error": str(comments_error)}
        status = comments_error.status
    except Exception as exception:
        logger.error('Exception add_rating_vote_to_comment: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@comments.route('/<comment_id>/disable', methods=['PUT'])
@admin_required
def put_comment_disabled(comment_id):
    try:
        comment_dto = comment_service.disable_comment(comment_id)
        if comment_dto is CommentDto.NULL:
            raise CommentsError("comment was not enabled", status=HTTPStatus.BAD_REQUEST)
        else:
            message = {}
            status = HTTPStatus.NO_CONTENT
    except CommentsError as comments_error:
        message = {"error": str(comments_error)}
        status = comments_error.status
    except Exception as exception:
        logger.error('Exception add_rating_vote_to_comment: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@comments.route('/<comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    try:
        comment_dto = comment_service.delete_comment(comment_id)
        if comment_dto is CommentDto.NULL:
            raise CommentsError("comment was not deleted", status=HTTPStatus.BAD_REQUEST)
        else:
            message = comment_dto.to_dict()
            status = HTTPStatus.OK
    except CommentsError as comments_error:
        message = {"error": str(comments_error)}
        status = comments_error.status
    except Exception as exception:
        logger.error('Exception add_rating_vote_to_comment: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
