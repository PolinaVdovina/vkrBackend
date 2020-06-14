
from datetime import datetime, timedelta
from flask import request, jsonify
from flask_restful import Resource
from core import get_database, get_database_session
from core.models import Position, Organization, Enterprise, WorkGroup, Executor, WorkTask

class GetExecutorsAnal(Resource):
    def post(self):
        json_data = request.get_json()
        id_chief = json_data['id']
        work_group = get_database_session().query(WorkGroup).filter(WorkGroup.id_chief == id_chief).first()
        work_group_id = work_group.id
        workers_list = get_database_session().query(Executor).filter(Executor.id_work_group == work_group_id).all()
        mass_result = []
        for worker in workers_list:
            temp = {'name': worker.name, 'time_sr': timedelta(), 'amount': 0, 'amount_delay': 0, 'amount_refuse': 0}
            list = get_database_session().query(WorkTask).filter(WorkTask.id_executor == worker.id).all()
            time_sum = timedelta()
            time_num = 0
            time_sr = 0
            for el in list:
                if el.date_start is not None and el.date_end is not None:
                    time_sum += el.date_end - el.date_start
                    time_num += 1
            if time_num != 0:
                time_sr = (time_sum / time_num)
            temp['time_sr'] = str(time_sr)
            temp['amount_delay'] = 0
            for el in list:
                if el.delay_reason is not None and el.date_start is not None:
                    temp['amount_delay'] += 1
            temp['amount_refuse'] = 0
            for el in list:
                if el.delay_reason is not None and el.date_start is None:
                    temp['amount_refuse'] += 1
            temp['amount'] = len(list) - temp['amount_refuse'] - temp['amount_delay']
            mass_result.append(temp)
        return jsonify(mass_result)

class GetWorkGroupsAnal(Resource):
    def post(self):
        json_data = request.get_json()
        work_groups = get_database_session().query(WorkGroup).all()
        mass_result = []
        for wg in work_groups:
            temp = {'name': wg.value, 'time_sr': timedelta(), 'amount': 0, 'amount_delay': 0, 'amount_refuse': 0}
            list = get_database_session().query(WorkTask).filter(WorkTask.Work_group == wg).all()
            time_sum = timedelta()
            time_num = 0
            time_sr = 0
            for el in list:
                if el.date_start is not None and el.date_end is not None:
                    time_sum += el.date_end - el.date_start
                    time_num += 1
            if time_num != 0:
                time_sr = time_sum / time_num
            temp['time_sr'] = str(time_sr)
            temp['amount_delay'] = 0
            for el in list:
                if el.delay_reason is not None and el.date_start is not None:
                    temp['amount_delay'] += 1
            temp['amount_refuse'] = 0
            for el in list:
                if el.delay_reason is not None and el.date_start is None:
                    temp['amount_refuse'] += 1
            temp['amount'] = len(list) - temp['amount_refuse'] - temp['amount_delay']
            mass_result.append(temp)
        return jsonify(mass_result)

