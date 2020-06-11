from flask import request, jsonify
from flask_restful import Resource
from core import get_database, get_database_session
from core.models import Position, Organization, Enterprise, WorkGroup, Executor, User


class GetPositions(Resource):
    def get(self):
        positions = get_database_session().query(Position).all()
        return jsonify([position.to_basic_dictionary() for position in positions])


class GetOrganizations(Resource):
    def get(self):
        organizations = get_database_session().query(Organization).all()
        return jsonify([organization.to_basic_dictionary() for organization in organizations])


class GetEnterprises(Resource):
    def get(self):
        enterprises = get_database_session().query(Enterprise).all()
        return jsonify([enterprise.to_basic_dictionary() for enterprise in enterprises])

class GetWorkGroups(Resource):
    def get(self):
        work_groups = get_database_session().query(WorkGroup).all()
        return jsonify([work_group.to_basic_dictionary() for work_group in work_groups])

class GetExecutors(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            id_chief = json_data['id']
            work_group = get_database_session().query(WorkGroup).filter(WorkGroup.id_chief == id_chief).first()
            work_group_id = work_group.id
            workers_list = get_database_session().query(Executor).filter(Executor.id_work_group == work_group_id).all()
            return jsonify([worker.to_basic_dictionary() for worker in workers_list])
        except:
            workers_list = get_database_session().query(Executor).all()
            return jsonify([worker.to_basic_dictionary() for worker in workers_list])

class GetUsers(Resource):
    def get(self):
        users_list = workers_list = get_database_session().query(User).all()
        return jsonify([user.to_basic_dictionary() for user in users_list])