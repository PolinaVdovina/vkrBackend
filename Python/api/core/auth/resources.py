from random import random
import jwt
from Tools.scripts.parse_html5_entities import get_json
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from core import get_database, get_database_session
from core.models import Employee, Role, Executor, User, json_to_model, WorkGroup
from core.auth.jwt import check_validation, check_validation_with_user, check_role_validation



'''class CheckUser(Resource):
    @check_validation_with_user
    def post(self, user):
        return jsonify({'msg': 'OK', 'user_id':user.id})'''



class UserLogin(Resource):
    def post(self):
        json_data = request.get_json()
        if 'login' not in json_data:
            return {"msg": "NO_LOGIN"}

        login = json_data['login']
        password = ''
        if 'password' in json_data:
            password = json_data['password']
        user = get_database_session().query(Employee).filter(Employee.login == login).first()

        if user:
            is_password_ok = False
            if password == '':
                if user.password_hash == None:
                    is_password_ok = True
            elif user.password_hash != None:
                password_hash = generate_password_hash(password)
                is_password_ok = check_password_hash(user.password_hash, password)
            if is_password_ok:
                access_token = user.access_token
                return jsonify({"msg": "OK", "login": login, "access_token": access_token, "role": user.role.value, "user_id": user.id})
            else:
                return jsonify({"msg": "WRONG_PASSWORD"})
        else:
            return jsonify({"msg": "WRONG_LOGIN",})


class UserRegister(Resource):
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
        if 'role' in json_data:
            role = json_data['role']
            if role == 'user':
                find_user = get_database_session().query(User).filter(User.login == login).first()
                if find_user:
                    return jsonify({"msg": "NOT_ORIGINAL_LOGIN"})
                else:
                    user = User(login=login, password_hash=password_hash, role_id=get_database_session().query(Role).filter(Role.value == role).first().id)
                    get_database().session.add(user)
                    get_database().session.commit()
            elif role == 'engineer' or role == 'dispatcher':
                find_user = get_database_session().query(Executor).filter(Executor.login == login).first()
                if find_user:
                    return jsonify({"msg": "NOT_ORIGINAL_LOGIN"})
                else:
                    user = Executor(login=login,
                                    password_hash=password_hash,
                                    role_id=get_database_session().query(Role).filter(Role.value == role).first().id)
                    get_database().session.add(user)
                    get_database().session.commit()
            else:
                find_user = get_database_session().query(Employee).filter(Employee.login == login).first()
                if find_user:
                    return jsonify({"msg": "NOT_ORIGINAL_LOGIN"})
                else:
                    user = Employee(login=login,
                                    password_hash=password_hash,
                                    role_id=get_database_session().query(Role).filter(Role.value == role).first().id)
                    get_database().session.add(user)
                    get_database().session.commit()
        else:
            return jsonify({"msg": "WRONG_ROLE"})

        return jsonify({"msg": "OK", "access_token": user.access_token,
                        "roles":  user.role.value})

class GetUser(Resource):
    def post(self):
        json_data = request.get_json()
        id = json_data['id']
        role = json_data['role'][0]
        if role == 'user':
            db_user = get_database_session().query(User).filter(User.id == id).first()
            return jsonify(db_user.to_basic_dictionary())
        elif role == 'engineer' or role == 'dispatcher':
            db_user = get_database_session().query(Executor).filter(Executor.id == id).first()
            return jsonify(db_user.to_basic_dictionary())
        elif role == 'supervisor':
            db_user = get_database_session().query(Employee).filter(Employee.id == id).first()
            id_group = get_database_session().query(WorkGroup).filter(WorkGroup.id_chief == id).first()
            json = db_user.to_basic_dictionary()
            if (id_group):
                json['id_work_group'] = id_group.id
            else:
                json['id_work_group'] = None
            return jsonify(json)
        else:
            return jsonify({"msg": "ROLE_ERROR"})


class UserUpdate(Resource):
    def post(self):
        json_data = request.get_json()
        if 'id' in json_data:
            id = json_data['id']
        else:
            id = json_data['user']['id']
        user = get_database_session().query(Employee).filter(Employee.id == id).first()
        role = get_database_session().query(Role).filter(Role.id == user.role_id).first().value


        if not user:
            return jsonify({"msg": "NO_USER_WITH_THIS_LOGIN"})

        if role == 'user':
            user = get_database_session().query(User).filter(User.id == id).first()
            json_to_model(json_data, user)
        elif role == 'engineer':
            user = get_database_session().query(Executor).filter(Executor.id == id).first()
            json_to_model(json_data, user)
        elif role == 'supervisor':
            id = json_data['user']['id']
            user = get_database_session().query(Employee).filter(Employee.id == id).first()
            id_group = json_data['id_work_group']
            if id_group:
                wg = get_database_session().query(WorkGroup).filter(WorkGroup.id == id_group).first()
                setattr(wg, 'id_chief', id)
                get_database_session().commit()
            json_to_model(json_data['user'], user)


        return jsonify({"msg": "OK"})







'''class ChangePassword(Resource):
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
        return jsonify({'msg': 'OK', 'access_token': create_access_token(user.create_access_token_payload())})'''









