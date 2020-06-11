from .resources import GetPositions, GetOrganizations, GetEnterprises, GetWorkGroups, GetExecutors, GetUsers


urls = [
    (GetPositions, '/api/positions_list'),
    (GetOrganizations, '/api/organizations_list'),
    (GetEnterprises, '/api/enterprises_list'),
    (GetWorkGroups, '/api/workgroups'),
    (GetExecutors, '/api/workers_list'),
    (GetUsers, '/api/users_list')
]