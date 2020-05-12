from flask_admin import Admin
from .flask import get_flask_app

admin = Admin(app=get_flask_app())


def init_admin():
    pass

