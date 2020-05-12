from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from core import get_database_session
from core.models import User


def check_login_validation(login, password):
    user = get_database_session().query(User).filter(User.login == login).first()
    if user:
        password_hash = generate_password_hash(password)
        is_password_ok = check_password_hash(user.password_hash, password)
        if is_password_ok:
            access_token = create_access_token(user.create_access_token_payload(), expires_delta=False)
            return ({"msg": "OK", "access_token": access_token, "user_id": user.id, 'user': user})
        else:
            return {"msg": "WRONG_PASSWORD"}
    else:
        return {"msg": "WRONG_LOGIN"}


def get_user_from_identity():
    identity = get_jwt_identity()
    if 'token_id' not in identity:
        return None


