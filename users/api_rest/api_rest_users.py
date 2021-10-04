from datetime import timedelta
from http import HTTPStatus

import colorlog
import json
from flask import Blueprint, Flask, Response, request
from flask_cors import cross_origin
from flask_login import login_user, logout_user, LoginManager, current_user

import config
from users.dto import UserDto
from users.role_required_decorators import admin_required, login_required
from users.services.user_service import UserService
from users.user_error import UserError

login_manager = LoginManager()
logger = colorlog.getLogger('REST API Users')
users = Blueprint('users', __name__)
user_service: UserService

MAX_SESSION_TIME_MINUTES = config.MAX_SESSION_TIME_MINUTES
SUPER_ADMIN_USERNAME = config.SUPER_ADMIN_USERNAME


@login_manager.user_loader
def load_user(user_id):
    user_dto: UserDto = user_service.get_user_by_id(user_id)
    return user_dto


@users.route("/all", methods=['GET'])
@admin_required
def get_all():
    file_list = user_service.get_all_users()
    user_array = []
    for element in file_list:
        user_array.append(element.to_dict())
    return Response(response=json.dumps({"users": user_array}), status=HTTPStatus.OK, mimetype="application/json")


@users.route("/login", methods=['POST'])
@cross_origin()
def login():
    try:
        data = json.loads(request.data)
        username = data['username']
        password = data['password']
        # if current_user.is_active:
        #     message = {'error': 'user already logged'}
        #     status = HTTPStatus.CONFLICT
        # else:
        user_dto: UserDto = user_service.login_user(username, password)
        if user_dto is UserDto.NULL:
            raise UserError('login error', status=HTTPStatus.FORBIDDEN)
        else:
            message = user_dto.to_dict()
            status = HTTPStatus.OK
            login_user(user_dto, remember=True, duration=timedelta(minutes=MAX_SESSION_TIME_MINUTES))

    except UserError as user_error:
        message = {"error": str(user_error)}
        status = user_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception login: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Response(
        response=json.dumps(message),
        status=status,
        mimetype="application/json")


@users.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return Response(
        response=json.dumps({}),
        status=HTTPStatus.OK,
        mimetype="application/json")


@users.route("/register", methods=['POST'])
def register():
    try:
        data = json.loads(request.data)
        username = data['username']
        password = data['password']
        email = data['email']
        name = data['name']
        birth_date = data['birth_date']
        user_dto: UserDto = user_service.register_user(
            username,
            password,
            email,
            name,
            False,
            birth_date)
        if user_dto is UserDto.NULL:
            raise UserError('register error', status=HTTPStatus.BAD_REQUEST)
        else:
            message = user_dto.to_dict()
            status = HTTPStatus.CREATED
    except UserError as user_error:
        message = {"error": str(user_error)}
        status = user_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception register: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@users.route("/admin", methods=['POST'])
@admin_required
def update_user():
    try:
        data = json.loads(request.data)
        user_id = data['user_id']
        is_admin = bool(data['admin'])
        if current_user.username == SUPER_ADMIN_USERNAME:
            user_dto = user_service.update_role_admin(user_id, is_admin)
        else:
            user_dto = user_service.update_role_user(user_id, is_admin)
        if user_dto is UserDto.NULL:
            raise UserError('update admin error', status=HTTPStatus.BAD_REQUEST)
        else:
            message = user_dto.to_dict()
            status = HTTPStatus.CREATED
    except UserError as user_error:
        message = {"error": str(user_error)}
        status = user_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception update user to admin: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )


@users.route("/delete/<user_id>", methods=['DELETE'])
@admin_required
def delete(user_id):
    try:
        if current_user.username == SUPER_ADMIN_USERNAME:
            user_dto: UserDto = user_service.delete_admin(user_id)
        else:
            user_dto: UserDto = user_service.delete_user(user_id)

        if user_dto is UserDto.NULL:
            raise UserError('user was not found', status=HTTPStatus.NOT_FOUND)
        else:
            message = user_dto.to_dict()
            status = HTTPStatus.OK

    except UserError as user_error:
        message = {"error": str(user_error)}
        status = user_error.status
    except ValueError:
        message = {"error": "parsing JSON error"}
        status = HTTPStatus.PRECONDITION_FAILED
    except Exception as exception:
        logger.error('Exception delete: ', exception)
        message = {"error": "exception"}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return Flask.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
