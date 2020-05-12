from random import random
import jwt
from Tools.scripts.parse_html5_entities import get_json
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from core import get_database, get_database_session
from core.models import User
from core.auth.jwt import check_validation, check_validation_with_user, check_role_validation


class CheckUser(Resource):
    @check_validation_with_user
    def post(self, user):
        return jsonify({'msg': 'OK', 'user_id':user.id})


class UserLogin(Resource):
    def post(self):
        json_data = request.get_json()
        if 'login' not in json_data:
            return {"msg": "NO_LOGIN"}

        login = json_data['login']
        password = ''
        if 'password' in json_data:
            password = json_data['password']
        user = get_database_session().query(User).filter(User.login == login).first()

        if user:
            is_password_ok = False
            if password == '':
                if user.password_hash == None:
                    is_password_ok = True
            elif user.password_hash != None:
                password_hash = generate_password_hash(password)
                is_password_ok = check_password_hash(user.password_hash, password)
            if is_password_ok:
                access_token = create_access_token(user.create_access_token_payload(), expires_delta=False)
                return jsonify({"msg": "OK", "access_token": access_token, "roles":  user.role_string_array})
            else:
                return jsonify({"msg": "WRONG_PASSWORD"})
        else:
            return jsonify({"msg": "WRONG_LOGIN",})


class UserRegister(Resource):
    @check_role_validation(roles = ['ChangeUser'])
    def post(self):
        json_data = request.get_json()
        if 'login' not in json_data:
            return jsonify({"msg": "NO_LOGIN"})

        password_hash = None
        if 'password' in json_data:
            password = ''
            password = json_data['password']
            if password != None:
                password_hash = generate_password_hash(password=password)

        login = json_data['login']
        find_user = get_database_session().query(User).filter(User.login == login).first()
        if find_user:
            return jsonify({"msg": "NOT_ORIGINAL_LOGIN"})


        if 'roles' in json_data:
            roles = json_data['roles']
            try:
                user = User(login=login, password_hash=password_hash, roles = Role.get_roles_from_string_array(roles))
                get_database().session.add(user)
                get_database().session.commit()
            except:
                return jsonify({"msg": "WRONG_ROLES"})
        else:
            user = User(login=login, password_hash=password_hash)
            get_database().session.add(user)
            get_database().session.commit()

        return jsonify({"msg": "OK", "access_token": create_access_token(user.create_access_token_payload(), expires_delta=False),
                        "roles":  user.role_string_array })


class UserDelete(Resource):
    @check_role_validation(roles = ['ChangeUser'])
    def post(self):
        json_data = request.get_json()
        if 'login' not in json_data:
            return jsonify({"msg": "NO_LOGIN"})
        login = json_data['login']
        find_user = get_database_session().query(User).filter(User.login == login).first()

        if not find_user:
            return jsonify({"msg": "NO_USER_WITH_THIS_LOGIN"})

        roles = find_user.roles
        if 'SuperUser' in roles:
            return jsonify({"msg": "Do you really wanna delete SuperUser??? This is madness!"})

        get_database_session().delete(find_user)
        get_database().session.commit()
        return jsonify({"msg": "OK"})




class ChangePassword(Resource):
    @check_role_validation(roles = ['ChangeUser'])
    def post(self):
        jwt = get_jwt_identity()
        json_data = request.get_json()
        if 'user_id' not in jwt:
            return jwt['msg': 'NO_USER_ID']
        if 'newPassword' not in json_data:
            return jsonify({'msg': 'NO_NEW_PASSWORD'})
        new_password = json_data['newPassword']
        user_id = jwt['user_id']
        user = get_database_session().query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({'msg': 'WRONG_USER'})
        new_password_hash = generate_password_hash(new_password)
        user.password_hash = new_password_hash
        user.token_id = User.token_seq_id.next_value()
        get_database_session().flush()
        get_database_session().commit()
        return jsonify({'msg': 'OK', 'access_token': create_access_token(user.create_access_token_payload())})









