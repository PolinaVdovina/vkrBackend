from .resources import UserLogin, UserRegister, CheckUser, ChangePassword


urls = [
    (UserLogin, '/api/auth/login'),
    (UserRegister, '/api/auth/register'),
    (CheckUser, '/api/auth/check'),
    (ChangePassword, '/api/auth/changepassword'),
]