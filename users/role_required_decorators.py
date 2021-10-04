import json
from functools import wraps
from http import HTTPStatus

from flask import Response
from flask_login import current_user
import config

SUPER_ADMIN_USERNAME = config.SUPER_ADMIN_USERNAME
SECURE_API = config.SECURE_API


def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if SECURE_API != 'True':
            return f(*args, **kws)
        if not current_user.is_active or not current_user.admin or not current_user.username == SUPER_ADMIN_USERNAME:
            return Response(
                response=json.dumps({'error': 'super admin required'}),
                status=HTTPStatus.UNAUTHORIZED,
                mimetype="application/json")
        return f(*args, **kws)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if SECURE_API != 'True':
            return f(*args, **kws)
        if not current_user.is_active or not current_user.admin:
            return Response(
                response=json.dumps({'error': 'login admin required'}),
                status=HTTPStatus.UNAUTHORIZED,
                mimetype="application/json")
        return f(*args, **kws)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if SECURE_API != 'True':
            return f(*args, **kws)
        if not current_user.is_active:
            return Response(
                response=json.dumps({'error': 'login required'}),
                status=HTTPStatus.UNAUTHORIZED,
                mimetype="application/json")
        return f(*args, **kws)

    return decorated_function


def admin_or_owner_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if SECURE_API != 'True':
            return f(*args, **kws)
        user_id = kws.get('user_id')
        if not current_user.is_active or user_id is None or user_id != current_user.id or not current_user.admin:
            return Response(
                response=json.dumps({'error': 'login admin or owner required'}),
                status=HTTPStatus.UNAUTHORIZED,
                mimetype="application/json")
        return f(*args, **kws)

    return decorated_function
