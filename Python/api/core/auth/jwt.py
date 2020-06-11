from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import get_database_session
from core.flask import get_flask_app
from core.models import Employee
from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from core import get_database_session, get_rest_api

_jwt = None        # type: JWTManager

def get_jwt() -> JWTManager:
    global _jwt
    if not _jwt:
        jwt = JWTManager(app=get_flask_app())
    return _jwt

def show_error_func(msg):
    return 'Authorization Error: ' + msg, 422

def check_validation(function):
    @wraps(function)
    @jwt_required
    def wrapper(*args, **kwargs):
        get_database_session()
        identity = get_jwt_identity()
        if 'user_id' not in identity:
            return show_error_func('no user_id in token')
        if 'token_id' not in identity:
            return show_error_func('no token_id in token')

        user = get_database_session().query(Employee).\
            filter(Employee.id == identity['user_id']).\
            filter(Employee.token_id == identity['token_id']).\
            first()

        if not user:
            return show_error_func('no user')


        return  function(*args, **kwargs)
    return wrapper


def check_validation_with_user(function):
    @wraps(function)
    @jwt_required
    def wrapper(*args, **kwargs):
        get_database_session()
        identity = get_jwt_identity()
        if 'user_id' not in identity:
            return show_error_func('no user_id in token')
        if 'token_id' not in identity:
            return show_error_func('no token_id in token')

        user = get_database_session().query(Employee). \
            filter(Employee.id == identity['user_id']). \
            filter(Employee.token_id == identity['token_id']). \
            first()

        if not user:
            return show_error_func('no user')

        def with_user(user):
            return function(user=user, *args, **kwargs)

        return with_user(user)

    return wrapper


def check_role_validation(roles = []):
    def decorator(function):
        @wraps(function)
        @jwt_required
        def wrapper(*args, **kwargs):
            get_database_session()
            identity = get_jwt_identity()

            if 'user_id' not in identity:
                return show_error_func('no user_id in token')
            if 'token_id' not in identity:
                return show_error_func('no token_id in token')

            user = get_database_session().query(Employee). \
                filter(Employee.id == identity['user_id']). \
                filter(Employee.token_id == identity['token_id']). \
                first()
            user_roles = user.role_string_array
            if 'SuperUser' not in user_roles:
                for role in roles:
                    if role not in user_roles:
                        return show_error_func('role does not exist')


            if not user:
                return show_error_func('no user')

            return function(*args, **kwargs)
        return wrapper
    return decorator