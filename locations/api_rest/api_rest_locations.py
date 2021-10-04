from datetime import datetime
from http import HTTPStatus

import colorlog
import json
from flask import request, Blueprint, Flask

from locations.locations_error import LocationsError
from locations.dto import LocationDto
from locations.services.location_service import LocationService
from users.role_required_decorators import login_required
from users.services.user_service import UserService
from utils.coordinates import Coordinates

logger = colorlog.getLogger('REST API Locations')
locations = Blueprint('locations', __name__)
location_service: LocationService
user_service: UserService


@locations.route('', methods=['POST'])
@locations.route('/', methods=['POST'])
@login_required
def add_location():
    try:
        data = json.loads(request.data)
        is_active = bool(data['isActive'])
        type = data['type']
        subtype = data['subtype']
        title = data['title']
        description = data['description']
        coordinates = Coordinates(data['coordinates']['latitude'], data['coordinates']['longitude'])
        workers = data['workers']
        owner_user_id = data['ownerUserId']
        if 'mainVideoId' in data:
            main_video_id = data['mainVideoId']
        else:
            main_video_id = None

        location_dto: LocationDto = location_service.add(
            is_active,
            type,
            subtype,
            title,
            description,
            coordinates,
            workers,
            owner_user_id,
            main_video_id
        )
        if location_dto == LocationDto.NULL:
            logger.error("Location was not created")
            message = {"error": "location was not created"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = location_dto.to_dict()
            status = HTTPStatus.CREATED
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception adding location: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('/<location_id>', methods=['GET'])
@login_required
def get_location_by_id(location_id):
    try:
        location_dto: LocationDto = location_service.get(location_id)
        if location_dto == LocationDto.NULL:
            logger.error("Location was not found")
            message = {"error": "location was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:

            message = location_dto.to_dict()
            status = HTTPStatus.OK
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except Exception as exception:
        logger.error('Exception getting locations : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('', methods=['GET'])
@locations.route('/', methods=['GET'])
@login_required
def get_locations():
    try:
        params = {}
        if 'type' in request.args:
            params.update({'type': request.args.get('type')})
        if 'ownerUserId' in request.args:
            params.update({'owner_user_id': request.args.get('ownerUserId')})
        if 'subtype' in request.args:
            params.update({'subtype': request.args.get('subtype')})

        if params is {}:
            locations_dto = location_service.get_all()
        else:
            locations_dto = location_service.get_by_params(params)
        locations_string = []
        for location_dto in locations_dto:
            locations_string.append(location_dto.to_dict())

        message = locations_string
        status = HTTPStatus.OK
    except Exception as exception:
        logger.error('Exception getting locations : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR
    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('/<location_id>/active', methods=['PUT'])
@login_required
def set_location_active(location_id):
    try:
        location_dto = location_service.put_active(location_id)
        if location_dto is LocationDto.NULL:
            message = {"error": "location was not modified"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = location_dto.to_dict()
            status = HTTPStatus.OK
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception setting location active: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('/<location_id>/inactive', methods=['PUT'])
@login_required
def set_location_inactive(location_id):
    try:
        location_dto = location_service.put_inactive(location_id)
        if location_dto is LocationDto.NULL:
            message = {"error": "location was not modified"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = location_dto.to_dict()
            status = HTTPStatus.OK
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception setting location inactive: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('/<location_id>', methods=['PATCH'])
@login_required
def update_location(location_id):
    try:
        data = json.loads(request.data)
        is_active = bool(data['isActive'])
        type = data['type']
        subtype = data['subtype']
        title = data['title']
        description = data['description']
        latitude = data['coordinates']['latitude']
        longitude = data['coordinates']['longitude']
        workers = data['workers']
        owner_user_id = data['ownerUserId']
        if 'mainVideoId' in data:
            main_video_id = data['mainVideoId']
        else:
            main_video_id = None
        # creation_date_str = data['creationDate']
        # creation_date = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%S')

        location_dto: LocationDto = location_service.update(location_id,
                                                            is_active,
                                                            type,
                                                            subtype,
                                                            title,
                                                            description,
                                                            latitude,
                                                            longitude,
                                                            workers,
                                                            owner_user_id,
                                                            main_video_id)
        if location_dto == LocationDto.NULL:
            logger.error("Location was not updated")
            message = {"error": "location was not updated"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = location_dto.to_dict()
            status = HTTPStatus.CREATED
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception updating location: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@locations.route('/<location_id>', methods=['DELETE'])
@login_required
def delete_location(location_id):
    try:
        location_dto: LocationDto = location_service.delete(location_id)
        if location_dto is LocationDto.NULL:
            message = {"error": "location was not deleted"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = location_dto.to_dict()
            status = HTTPStatus.OK
    except LocationsError as location_error:
        message = {"error": str(location_error)}
        status = location_error.status
    except Exception as exception:
        logger.error('Exception deleting location: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
