import os
import re
from http import HTTPStatus

from flask import request, make_response, send_file, abort, Blueprint, Flask, Response
import colorlog, json
from geopy.distance import great_circle
# from websocket import create_connection
from storage.storage_error import StorageError
from storage.storage_service import StorageService
from users.role_required_decorators import admin_required, login_required
from utils.json_response import json_response
from video_catalog.dto import FileStatus, VideoDto

logger = colorlog.getLogger('API REST Storage')
storage_service: StorageService
analyzer_service = None
MAX_FILE_SIZE_BYTES = 524288000

storage = Blueprint('storage', __name__)


@storage.route("/<place_id>", methods=['POST'])
def upload_video(place_id):
    if 'file' not in request.files:
        logger.error("File not in request.")
        message = "file was not found"
        status = HTTPStatus.BAD_REQUEST
    else:
        logger.debug("Uploading File: {} of {}".format(place_id, None))
        file = request.files['file']
        if file:
            if os.fstat(file.fileno()).st_size > MAX_FILE_SIZE_BYTES:
                message = "file 500_mb_max"
                status = HTTPStatus.PRECONDITION_FAILED
            elif not re.compile('([a-zA-Z0-9\s_\.\-\(\):])*').match(file.filename):
                message = "error_file_name_chars"
                status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            else:
                file_dto = storage_service.upload_file(place_id, file, None)
                if file_dto is VideoDto.NULL:
                    message = "not_uploaded"
                    status = HTTPStatus.BAD_REQUEST
                else:
                    message = file_dto.to_dict()
                    status = HTTPStatus.CREATED
                    # ws.send('New video ' + file_dto.g_path)
        else:
            logger.error("File not in request")
            message = "file was not found"
            status = HTTPStatus.BAD_REQUEST

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@storage.route("/image", methods=['POST'])
@login_required
def upload_simple_file():
    if 'file' not in request.files:
        logger.error("File was not found in request")
        message = json_response(info="not_file")
        status = HTTPStatus.BAD_REQUEST
    else:
        file = request.files['file']
        if file:
            if os.fstat(file.fileno()).st_size > MAX_FILE_SIZE_BYTES:
                message = "file 500_mb_max"
                status = HTTPStatus.PRECONDITION_FAILED
            elif not re.compile('([a-zA-Z0-9\s_\.\-\(\):])*').match(file.filename):
                message = "error_file_name_chars"
                status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            else:
                public_url_image = storage_service.upload_simple_file('images', file)
                if public_url_image is None:
                    message = "not_uploaded"
                    status = HTTPStatus.BAD_REQUEST
                else:
                    message = json_response(url=public_url_image)
                    status = HTTPStatus.CREATED
        else:
            logger.error("File not in request")
            message = "file was not found"
            status = HTTPStatus.BAD_REQUEST

    return Flask.response_class(
        response=message,
        status=status,
        mimetype='application/json'
    )


# TODO remove
@storage.route('/<path:path_file>', methods=['GET'])
@login_required
def get_file(path_file):
    path = storage_service.get_file(path_file)
    if path is not None:
        try:
            response = make_response(send_file(path))
        except PermissionError:
            logger.error('File: ' + path + ' private')
            response = abort(HTTPStatus.UNAUTHORIZED)
    else:
        logger.info('File: ' + path_file + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return response


@storage.route('/public/<video_id>', methods=['PUT'])
def put_public(video_id):
    logger.debug("Putting public video with ID: " + video_id)
    file_dto = storage_service.make_file_public(video_id)
    if file_dto is not None and file_dto is not VideoDto.NULL:
        response = str(file_dto)  # FIXME to_dict()
        # notification = '{"notification": "' + str(FileStatus(file_dto.file_status)) + '"}'
        # ws.send(notification)
    else:
        logger.info('File with id: ' + video_id + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return Response(response=response, status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/private/<video_id>', methods=['PUT'])
@login_required
def put_private(video_id):
    logger.debug("Putting private video with ID: " + video_id)
    file_dto = storage_service.make_file_private(video_id)
    if file_dto is not None:
        response = str(file_dto)  # FIXME to_dict()
    else:
        logger.info('File with id: ' + video_id + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return Response(response=response, status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/rev/<video_id>', methods=['PUT'])
@login_required
def put_rev_required(video_id):
    file_dto = storage_service.make_file_to_rev(video_id)
    if file_dto is not VideoDto.NULL:
        response = str(file_dto)  # FIXME to dict
    else:
        logger.info('File with id: ' + video_id + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return Response(response=response, status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/delete/<video_id>', methods=['PUT'])
@login_required
def to_delete(video_id):
    file_dto = storage_service.delete_file(video_id)
    return Response(response=str(file_dto), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/<video_id>', methods=['DELETE'])
def permanent_delete(video_id):
    file_dto = storage_service.permanent_delete(video_id)
    return Response(response=str(file_dto), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/undelete/<video_id>', methods=['PUT'])
def undelete(video_id):  # FIXME incorrect word undelete
    file_dto = storage_service.undelete_file(video_id)
    return Response(response=str(file_dto), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/list/place/<place_id>', methods=['GET'])
def list_files_by_place(place_id):
    file_list = storage_service.list_videos_by_place(place_id)
    return Response(response=json.dumps(file_list), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/list/user/<user_id>', methods=['GET'])
def list_files_by_user(user_id):
    file_list = storage_service.list_videos_by_user(user_id)
    return Response(response=json.dumps(file_list), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/list', methods=['GET'])
def list_videos():
    file_list = storage_service.list_videos()
    return Response(response=json.dumps(file_list), status=HTTPStatus.OK, mimetype="application/json")


@storage.route('/list/search', methods=['POST'])
def list_search_videos():
    try:
        body = json.loads(request.data)
        place_ids = body['place_id']
        video_list = storage_service.list_videos_by_places(place_ids)
        message = video_list
        status = HTTPStatus.OK
    except StorageError as storage_error:
        message = {"error": str(storage_error)}
        status = storage_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception getting caminatas : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@storage.route('/id/<video_id>', methods=['GET'])
def get_file_by_id(video_id):
    path = storage_service.get_file_id(video_id)
    logger.debug("Get File ID: " + str(path))
    if path is not None:
        try:
            response = make_response(send_file(path))
        except PermissionError:
            logger.error('File: ' + path + ' private')
            response = abort(HTTPStatus.UNAUTHORIZED)
    else:
        logger.info('File: ' + video_id + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return response


@storage.route('/video_id/<video_id>', methods=['GET'])
def get_video_id(video_id):
    video_dto = storage_service.get_video_id(video_id)
    if video_dto is VideoDto.NULL:
        logger.error("Video was not found")
        message = {"error": "video was not found"}
        status = HTTPStatus.BAD_REQUEST
    else:
        message = video_dto.to_dict()
        status = HTTPStatus.OK
    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@storage.route('/register', methods=['POST'])
def register_user_to_video():
    try:
        data = json.loads(request.data)
        name = data['name']
        video_id = data['videoId']
        user_id = data['user_id']
        description = data['description']
        title = data['title']
        place_id = data['place_id']
        latitude = data['coordinates']['latitude']
        longitude = data['coordinates']['longitude']
        video_dto: VideoDto = storage_service.update_file(video_id,
                                                          user_id,
                                                          place_id,
                                                          title,
                                                          description,
                                                          name,
                                                          latitude,
                                                          longitude)
        if video_dto is VideoDto.NULL:
            message = {"error": "error updating video"}
            status = HTTPStatus.NOT_FOUND
        else:
            # if point != video_dto.place_id:
            #     logger.error("Different place name in register")
            message = video_dto.to_dict()
            status = HTTPStatus.CREATED

    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception register_user_video: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@storage.route('/analysis/<video_id>', methods=['GET'])
def get_file_analysis_id(video_id):
    analysis_file = storage_service.get_file_analysis_id(video_id)
    if analysis_file is not None:
        try:
            response = make_response(send_file(analysis_file))
        except PermissionError:
            logger.error('File analysis of: ' + video_id + ' private')
            response = abort(HTTPStatus.UNAUTHORIZED)
    else:
        logger.info('File: ' + video_id + ' not found')
        response = abort(HTTPStatus.NOT_FOUND)
    return response

# FIXME
# @new_storage.route('/list_gcs', methods=['GET'])
# def list_videos_gcs():
#     data = storage_service.list_videos_gcs()
#     return Response(response=json.dumps(data), status=HTTPStatus.OK, mimetype="application/json")
