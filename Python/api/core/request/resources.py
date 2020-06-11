from Tools.scripts.parse_html5_entities import get_json
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import false, true
from werkzeug.security import generate_password_hash, check_password_hash
from core import get_database, get_database_session
from core.models import Employee, Role, Executor, User, json_to_model, WorkGroup, Incident, WorkTask
from core.auth.jwt import check_validation, check_validation_with_user, check_role_validation

class GetUserTable(Resource):
    def post(self):
        json_data = request.get_json()
        id = json_data['id']
        type = json_data['type']
        incidents = get_database_session().query(Incident).filter(Incident.id_user == id).all()
        ids = []
        for inc in incidents:
            ids.append(inc.id)
        if type == 'in_works':
            incidents_inwork = []
            for inc in incidents:
                if inc.id_status != 2:
                    incidents_inwork.append(inc)
            return jsonify([incident.to_basic_dictionary() for incident in incidents_inwork])
        elif type == 'will_estimate':
            worktasks = []
            for id_inc in ids:
                #worktasks = get_database_session().query(WorkTask).filter(WorkTask.id_incident in ids).all()
                temp = get_database_session().query(WorkTask).filter((WorkTask.id_incident == id_inc)\
                                                                     &(WorkTask.rating_user == None)\
                                                                     &(WorkTask.date_end != None)).all()
                worktasks.extend(temp)
            return jsonify([worktask.to_basic_dictionary() for worktask in worktasks])
        elif type == 'complete':
            worktasks = []
            for id_inc in ids:
                temp = []
                temp = get_database_session().query(WorkTask).filter((WorkTask.id_incident == id_inc)\
                                                                     &(WorkTask.rating_user!=None)\
                                                                     &(WorkTask.date_end != None)).all()
                worktasks.extend(temp)
            return jsonify([worktask.to_basic_dictionary() for worktask in worktasks])


class CreateIncident(Resource):
    def post(self):
        json_data = request.get_json()
        id_user = json_data['id_user']
        id_method = json_data['id_method']
        id_status = json_data['id_status']
        date_reg = json_data['date_reg']
        description = json_data['description']
        new_incident = Incident(id_user=id_user, id_method=id_method, id_status=id_status, date_reg=date_reg, description=description)
        get_database().session.add(new_incident)
        get_database().session.commit()


class SetRating(Resource):
    def post(self):
        json_data = request.get_json()
        id_wt = json_data['id']
        rating_user = json_data['rating']
        worktask = get_database_session().query(WorkTask).filter(WorkTask.id == id_wt).first()
        worktask.rating_user = rating_user
        id_exec = worktask.id_executor
        executor = get_database_session().query(Executor).filter(Executor.id == id_exec).first()
        wt_exec = get_database_session().query(WorkTask).filter((WorkTask.id_executor == id_exec) & (WorkTask.rating_user != None)).all()
        sum = 0
        for wt in wt_exec:
            sum += float(wt.rating_user)
        rating_exec_new = sum / len(wt_exec)
        executor.rating_user = rating_exec_new
        get_database_session().commit()

class GetEngineerTable(Resource):
    def post(self):
        json_data = request.get_json()
        id = json_data['id']
        type = json_data['type']
        tasks = get_database_session().query(WorkTask).filter(WorkTask.id_executor == id).all()
        if type == 'new':
            result = []
            for wt in tasks:
                if wt.date_start is None and wt.delay_reason is None:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])
        elif type == 'in_work':
            result = []
            for wt in tasks:
                if wt.date_end is None and wt.date_start is not None:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])
        elif type == 'complete':
            result = []
            for wt in tasks:
                if wt.date_end is not None:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])


class UpdateWorkTask(Resource):
    def post(self):
        json_data = request.get_json()
        id = json_data['id']
        worktask = get_database_session().query(WorkTask).filter(WorkTask.id == id).first()
        if 'description' in json_data:
            description = json_data['description']
            worktask.description = description
        if 'date_end' in json_data:
            date_end = json_data['date_end']
            worktask.date_end = date_end
        if 'id_work_group' in json_data:
            id_work_group = json_data['id_work_group']
            worktask.id_work_group = id_work_group
        if 'id_executor' in json_data:
            id_executor = json_data['id_executor']
            worktask.id_executor = id_executor
        if 'solution' in json_data:
            solution = json_data['solution']
            worktask.solution = solution
        if 'rating' in json_data:
            rating = json_data['rating']
            worktask.rating_isp = rating
            id_inc = worktask.id_incident
            incid = get_database_session().query(Incident).filter(Incident.id == id_inc).first()
            id_user = incid.id_user
            user = get_database_session().query(User).filter(User.id == id_user).first()
            incidents = get_database_session().query(Incident).filter(Incident.id_user == id_user).all()
            ids = []
            for inc in incidents:
                ids.append(inc.id)
            worktasks = []
            for id_inc in ids:
                temp = get_database_session().query(WorkTask).filter((WorkTask.id_incident == id_inc) & (WorkTask.rating_isp != None)).all()
                worktasks.extend(temp)
            sum_rating = 0
            num_rating = 0
            for wt in worktasks:
                sum_rating += wt.rating_isp
                num_rating += 1
            if num_rating != 0:
                user_rating = sum_rating / num_rating
                user.rating = user_rating
        if 'id_incident' in json_data:
            id_incident = json_data['id_incident']
            worktask.id_incident = id_incident
        if 'date_start' in json_data:
            date_start = json_data['date_start']
            worktask.date_start = date_start
        if 'date_deadline' in json_data:
            date_deadline = json_data['date_deadline']
            worktask.date_deadline = date_deadline
        if 'delay_reason' in json_data:
            delay_reason = json_data['delay_reason']
            worktask.delay_reason = delay_reason
        if 'priority' in json_data:
            priority = json_data['priority']
            worktask.priority = priority
        get_database_session().commit()


class GetDispatcherTable(Resource):
    def post(self):
        json_data = request.get_json()
        type = json_data['type']
        tasks = get_database_session().query(WorkTask).filter(WorkTask.id_executor != None).all()
        if type == 'in_process':
            inc_list = get_database_session().query(Incident).all()
            inc_in_process = []
            for inc in inc_list:
                wt_list = get_database_session().query(WorkTask).filter(WorkTask.Incident == inc).all()
                if len(wt_list) == 0:
                    inc_in_process.append(inc)
            return jsonify([incident.to_basic_dictionary() for incident in inc_in_process])
        elif type == 'appointed':
            return jsonify([worktask.to_basic_dictionary() for worktask in tasks])
        elif type == 'refuse':
            result = []
            for wt in tasks:
                if wt.date_end is None and wt.date_start is None and wt.delay_reason is not None:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])
        elif type == 'delay':
            result = []
            for wt in tasks:
                if wt.date_start is not None and wt.delay_reason is not None:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])
        elif type == 'arbitr':
            result = []
            for wt in tasks:
                if wt.rating_user is not None and wt.rating_isp is not None and wt.rating_user < 3.0 and wt.rating_isp < 3.0:
                    result.append(wt)
            return jsonify([worktask.to_basic_dictionary() for worktask in result])
