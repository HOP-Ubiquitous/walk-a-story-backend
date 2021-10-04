from http import HTTPStatus

import colorlog
import json
from flask import request, Blueprint, Flask

from caminatas.caminatas_error import CaminatasError
from caminatas.dto import CaminataDto
from caminatas.services.caminata_service import CaminataService
from users.dto import UserDto
from users.role_required_decorators import admin_required, login_required
from users.services.user_service import UserService
from users.user_error import UserError

logger = colorlog.getLogger('REST API Caminatas')
caminatas = Blueprint('caminatas', __name__)
caminatas_service: CaminataService
user_service: UserService


@caminatas.route('', methods=['POST'])
@caminatas.route('/', methods=['POST'])
@admin_required
def add_caminata():
    try:
        data = json.loads(request.data)
        title = data['title']
        description = data['description']
        date = data['date']
        image = data['image']
        place_id = data['place_id']
        address = data['address']
        latitude = data['coordinates']['latitude']
        longitude = data['coordinates']['longitude']
        user_id = data['user']['id']
        participants = data['participants']
        caminata_dto: CaminataDto = caminatas_service.add(title,
                                                          description,
                                                          date,
                                                          image,
                                                          place_id,
                                                          address,
                                                          latitude,
                                                          longitude,
                                                          user_id,
                                                          participants)
        if caminata_dto == CaminataDto.NULL:
            logger.error("Caminata was not created")
            message = {"error": "caminata was not created"}
            status = HTTPStatus.BAD_REQUEST
        else:
            user_dto: UserDto = user_service.get_user_by_id(user_id)
            if user_dto is UserDto.NULL:
                caminata_dto.user = 'undefined'
            else:
                caminata_dto.user = user_dto.to_dict()
            message = caminata_dto.to_dict()
            status = HTTPStatus.CREATED
    except UserError as user_error:
        message = {"error": str(user_error)}
        status = user_error.status
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as e:
        logger.error('Exception adding caminata: ', e)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/<caminata_id>', methods=['GET'])
@login_required
def get_caminata_by_id(caminata_id):
    try:
        caminata_dto: CaminataDto = caminatas_service.get_caminata_by_id(caminata_id)
        if caminata_dto == CaminataDto.NULL:
            logger.error("Caminata was not found")
            message = {"error": "caminata was not found"}
            status = HTTPStatus.BAD_REQUEST
        else:
            if request.args.get('option') == 'participants':

                participants = caminata_dto.participants
                participants_string = []
                for participant_id in participants:
                    try:
                        user_dto: UserDto = user_service.get_user_by_id(participant_id)
                        if user_dto is not UserDto.NULL:
                            participants_string.append(user_dto.to_dict())
                    except UserError as user_error:
                        logger.warning('Participant {} ignored, error: {}'.format(participant_id, user_error))
                caminata_dto.participants = participants_string

            user_dto: UserDto = user_service.get_user_by_id(caminata_dto.user)
            if user_dto is UserDto.NULL:
                caminata_dto.user = "undefined"
            else:
                caminata_dto.user = user_dto.to_dict()
            message = caminata_dto.to_dict()
            status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except Exception as exception:
        logger.error('Exception getting caminatas : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('', methods=['GET'])
@caminatas.route('/', methods=['GET'])
@login_required
def get_caminatas():
    try:
        caminatas_dto = caminatas_service.get_all()
        caminatas_dto_user = []
        for caminata_dto in caminatas_dto:
            user_dto = user_service.get_user_by_id(caminata_dto.user)
            if user_dto is UserDto.NULL:
                caminata_dto.user = 'undefined'
            else:
                caminata_dto.user = user_dto
            caminatas_dto_user.append(caminata_dto)
        caminatas_string = []
        for caminata_dto in caminatas_dto_user:
            caminatas_string.append(caminata_dto.to_dict())
        message = caminatas_string
        status = HTTPStatus.OK
    except Exception as exception:
        logger.error('Exception getting caminatas : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR
    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/place/<place_id>', methods=['GET'])
@login_required
def get_caminatas_by_place_id(place_id):
    try:
        caminatas_dto = caminatas_service.get_caminatas_by_place(place_id)
        caminatas_dto_user = []
        for caminata_dto in caminatas_dto:
            user_dto = user_service.get_user_by_id(caminata_dto.user)
            if user_dto is UserDto.NULL:
                caminata_dto.user = 'undefined'
            else:
                caminata_dto.user = user_dto
            caminatas_dto_user.append(caminata_dto)
        caminatas_string = []
        for caminata_dto in caminatas_dto_user:
            caminatas_string.append(caminata_dto.to_dict())
        message = caminatas_string
        status = HTTPStatus.OK
    except Exception as exception:
        logger.error('Exception getting caminatas : ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR
    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/registered/<user_id>', methods=['GET'])
@login_required
def get_caminatas_by_registrar(user_id):
    try:
        caminatas_dto = caminatas_service.get_caminatas_by_user(user_id)
        caminatas_dto_user = []
        for caminata_dto in caminatas_dto:
            user_dto = user_service.get_user_by_id(caminata_dto.user)
            if user_dto is UserDto.NULL:
                caminata_dto.user = 'undefined'
            else:
                caminata_dto.user = user_dto
            caminatas_dto_user.append(caminata_dto)
        caminatas_json = []
        for caminata_dto in caminatas_dto_user:
            caminatas_json.append(caminata_dto.to_dict())
        message = caminatas_json
        status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
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


@caminatas.route('/participant/<user_id>', methods=['GET'])
@login_required
def get_caminatas_by_participant(user_id):
    try:
        caminatas_dto = caminatas_service.get_caminatas_by_participant_user(user_id)
        caminatas_dto_user = []
        for caminata_dto in caminatas_dto:
            user_dto = user_service.get_user_by_id(caminata_dto.user)
            if user_dto is UserDto.NULL:
                caminata_dto.user = 'undefined'
            else:
                caminata_dto.user = user_dto
            caminatas_dto_user.append(caminata_dto)
        caminatas_json = []
        for caminata_dto in caminatas_dto_user:
            caminatas_json.append(caminata_dto.to_dict())
        message = caminatas_json
        status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
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


@caminatas.route('/<caminata_id>/participant', methods=['PUT'])
@login_required
def put_participant_caminata(caminata_id):
    try:
        data = json.loads(request.data)
        user_id = data['user_id']
        caminata_dto: CaminataDto = caminatas_service.put_participant(caminata_id, user_id)
        if caminata_dto is CaminataDto.NULL:
            message = {"error": "caminata was not modified"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = caminata_dto.to_dict()
            status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception putting participant of caminata: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/<caminata_id>/participant', methods=['DELETE'])
@login_required
def delete_participant_caminata(caminata_id):
    try:
        data = json.loads(request.data)
        user_id = data['user_id']
        caminata_dto: CaminataDto = caminatas_service.delete_participant(caminata_id, user_id)
        if caminata_dto is CaminataDto.NULL:
            logger.error("Caminata was not modified")
            message = {"error": "caminata was not modified"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = caminata_dto.to_dict()
            status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception deleting participant of caminata: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/<caminata_id>', methods=['PATCH'])
@admin_required
def update_caminata(caminata_id):
    try:
        data = json.loads(request.data)
        title = data['title']
        description = data['description']
        date = data['date']
        image = data['image']
        place_id = data['place_id']
        address = data['address']
        latitude = data['coordinates']['latitude']
        longitude = data['coordinates']['longitude']
        user_id = data['user']['id']
        caminata_dto: CaminataDto = caminatas_service.update(caminata_id,
                                                             title,
                                                             description,
                                                             date,
                                                             image,
                                                             place_id,
                                                             address,
                                                             latitude,
                                                             longitude,
                                                             user_id,
                                                             None)
        if caminata_dto is CaminataDto.NULL:
            logger.error("Caminata was not modified")
            message = {"error": "caminata was not modified"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = caminata_dto.to_dict()
            status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception deleting participant of caminata: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@caminatas.route('/<caminata_id>', methods=['DELETE'])
@admin_required
def delete_caminata(caminata_id):
    try:
        caminata_dto: CaminataDto = caminatas_service.delete(caminata_id)
        if caminata_dto is CaminataDto.NULL:
            message = {"error": "caminata was not deleted"}
            status = HTTPStatus.BAD_REQUEST
        else:
            message = caminata_dto.to_dict()
            status = HTTPStatus.OK
    except CaminatasError as caminata_error:
        message = {"error": str(caminata_error)}
        status = caminata_error.status
    except Exception as exception:
        logger.error('Exception deleting caminata: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
