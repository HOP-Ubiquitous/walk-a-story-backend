from http import HTTPStatus

from flask import request, Blueprint, Flask
import colorlog, json

from comments.services.comment_service import CommentService
from ratings.ratings_error import RatingsError
from ratings.dto import RatingDto
from ratings.services.rating_service import RatingService
from storage.storage_error import StorageError
from storage.storage_service import StorageService
from users.role_required_decorators import login_required, admin_required, admin_or_owner_user_required

logger = colorlog.getLogger('REST API Ratings')
rating_service: RatingService
comment_service: CommentService
storage_service: StorageService
DEFAULT_REPORT_VALUE = 1
ratings = Blueprint('ratings', __name__)


@ratings.route('/user/<user_id>', methods=['GET'])
@login_required
def get_rating_by_user_id(user_id):
    rating_dto_list = rating_service.get_rating_reports_by_user_id(user_id)
    rating_json_list = []
    for rating_dto in rating_dto_list:
        rating_json_list.append(rating_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(rating_json_list),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/comment/vote', methods=['POST'])
@login_required
def add_rating_vote_to_comment():
    try:
        data = json.loads(request.data)
        comment_id = data['comment_id']
        user_id = data['user_id']
        value = data['value']
        rating_dto: RatingDto = rating_service.add_rating_vote_to_comment(comment_id, user_id, value)
        if rating_dto != RatingDto.NULL:
            if value == 1:
                comment_service.add_positive_vote(comment_id)
            elif value == -1:
                comment_service.add_negative_vote(comment_id)
            else:
                raise RatingsError("value error, only 1 or -1", status=HTTPStatus.BAD_REQUEST)
        message = rating_dto.to_dict()
        status = HTTPStatus.CREATED
    except RatingsError as ratings_error:
        message = {"error": str(ratings_error)}
        status = ratings_error.status
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


@ratings.route('/comment/report', methods=['POST'])
@login_required
def add_rating_report_to_comment():
    try:
        data = json.loads(request.data)
        comment_id = data['comment_id']
        user_id = data['user_id']
        rating_dto: RatingDto = rating_service.add_rating_report_to_comment(comment_id, user_id)
        if rating_dto != RatingDto.NULL:
            comment_service.add_report(comment_id)
        message = rating_dto.to_dict()
        status = HTTPStatus.CREATED
    except RatingsError as ratings_error:
        message = {"error": str(ratings_error)}
        status = ratings_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception add_rating_report_to_comment: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/video/vote', methods=['POST'])
@login_required
def add_rating_vote_to_video():
    try:
        data = json.loads(request.data)
        video_id = data['video_id']
        user_id = data['user_id']
        value = data['value']
        rating_dto: RatingDto = rating_service.add_rating_vote_to_video(video_id, user_id, value)
        if rating_dto != RatingDto.NULL:
            storage_service.put_vote_video(video_id, value)
        message = rating_dto.to_dict()
        status = HTTPStatus.CREATED
    except RatingsError as ratings_error:
        message = {"error": str(ratings_error)}
        status = ratings_error.status
    except StorageError as storage_error:
        message = {"error": str(storage_error)}
        status = storage_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception add_rating_vote_to_video: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/video/report', methods=['POST'])
@login_required
def add_rating_report_to_video():
    try:
        data = json.loads(request.data)
        video_id = data['video_id']
        user_id = data['user_id']
        rating_dto: RatingDto = rating_service.add_rating_report_to_video(video_id, user_id)
        if rating_dto != RatingDto.NULL:
            storage_service.put_report_video(video_id, DEFAULT_REPORT_VALUE)
        message = rating_dto.to_dict()
        status = HTTPStatus.CREATED
    except RatingsError as ratings_error:
        message = {"error": str(ratings_error)}
        status = ratings_error.status
    except StorageError as storage_error:
        message = {"error": str(storage_error)}
        status = storage_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception add_rating_report_to_video: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


# FIXME
@ratings.route('/votes/user/<user_id>/comments/<comment_id>', methods=['GET'])
@admin_or_owner_user_required
def get_rating_votes_to_video_comments_by_user(user_id, comment_id):
    rating_dto_list = rating_service.get_rating_votes_to_video_comments_by_user(comment_id, user_id)
    rating_json_list = []
    for rating_dto in rating_dto_list:
        rating_json_list.append(rating_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(rating_json_list),
        status=status,
        mimetype='application/json'
    )


#  FIXME votes/user/{{user_id}}/comments/{{comment_id}}
@ratings.route('/reports/user/<user_id>/comments/<comment_id>', methods=['GET'])
@admin_or_owner_user_required
def get_rating_reports_to_video_comments_by_user(user_id, comment_id):
    rating_dto_list = rating_service.get_rating_reports_to_video_comments_by_user(comment_id, user_id)
    rating_json_list = []
    for rating_dto in rating_dto_list:
        rating_json_list.append(rating_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(rating_json_list),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/votes/user/<user_id>/video/<video_id>', methods=['GET'])
@admin_or_owner_user_required
def get_rating_votes_to_video_by_user(user_id, video_id):
    rating_dto_list = rating_service.get_rating_votes_to_video_by_user(video_id, user_id)
    rating_json_list = []
    for rating_dto in rating_dto_list:
        rating_json_list.append(rating_dto.to_dict())
    status = HTTPStatus.OK

    return Flask.response_class(
        response=json.dumps(rating_json_list),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/reports/user/<user_id>/video/<video_id>', methods=['GET'])
@admin_or_owner_user_required
def get_rating_reports_to_video_by_user(user_id, video_id):
    rating_dto_list = rating_service.get_rating_reports_to_video_by_user(video_id, user_id)
    rating_json_list = []
    for rating_dto in rating_dto_list:
        rating_json_list.append(rating_dto.to_dict())
    status = HTTPStatus.OK
    return Flask.response_class(
        response=json.dumps(rating_json_list),
        status=status,
        mimetype='application/json'
    )


@ratings.route('/<rating_id>', methods=['DELETE'])
@admin_required
def delete_rating(rating_id):
    try:
        rating_dto: RatingDto = rating_service.delete_rating(rating_id)
        if rating_dto is RatingDto.NULL:
            raise RatingsError("rating was not deleted", status=HTTPStatus.BAD_REQUEST)
        else:
            message = rating_dto.to_dict()
            status = HTTPStatus.OK
    except RatingsError as rating_error:
        message = {"error": str(rating_error)}
        status = rating_error.status
    except Exception as e:
        logger.error('Exception deleting rating: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
