from .resources import GetUserTable, CreateIncident, SetRating, GetEngineerTable, UpdateWorkTask, GetDispatcherTable, GetChiefTable


urls = [
    (GetUserTable, '/api/user_table'),
    (CreateIncident, '/api/create_new_inc'),
    (SetRating, '/api/set_rating'),
    (GetEngineerTable, '/api/engineer_table'),
    (UpdateWorkTask, '/api/update_work_task'),
    (GetDispatcherTable, '/api/disp_table'),
    (GetChiefTable, '/api/chief_table')
]