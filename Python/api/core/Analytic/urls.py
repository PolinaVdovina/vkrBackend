from .resources import GetExecutorsAnal, GetWorkGroupsAnal


urls = [
    (GetExecutorsAnal, '/api/workers_list_anal'),
    (GetWorkGroupsAnal, '/api/work_groups_list_anal')
]