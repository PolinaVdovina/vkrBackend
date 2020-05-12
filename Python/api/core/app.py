from flask import Flask
from flask_cors import CORS

from . import get_database
from .admin import init_admin
from .auth.jwt import get_jwt
from .flask import get_flask_app, get_rest_api
from .urls import urls


def configure_app(config):
    # init singletons
    get_flask_app()
    get_flask_app().config.from_object(config)
    get_database()
    get_rest_api()
    get_jwt()

    cors = CORS(get_flask_app(), resources={r"/api/*": {"origins": "*"}})

    init_admin()

    #
    for url in urls:
        get_rest_api().add_resource(url[0], url[1])


