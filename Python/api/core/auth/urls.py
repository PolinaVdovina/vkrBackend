from .resources import UserLogin, GetUser, UserRegister, UserUpdate  # , CheckUser, ChangePassword


urls = [
    (UserLogin, '/api/auth/login'),
    (UserRegister, '/api/auth/register'),
    (GetUser, '/api/cabinet'),
    (UserUpdate, '/api/update_user')
]


    #(CheckUser, '/api/auth/check'),
    #(ChangePassword, '/api/auth/changepassword'),