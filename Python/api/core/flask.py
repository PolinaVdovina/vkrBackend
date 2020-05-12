from flask import Flask
from flask_restful import Api

_flask_app = None  # type: Flask
_rest_api = None   # type: Api

def get_flask_app() -> Flask:
    global _flask_app
    if not _flask_app:
        _flask_app = Flask(__name__, static_folder="static")
    return _flask_app


def get_rest_api() -> Api:
    global _rest_api
    if not _rest_api:
        _rest_api = Api(app=get_flask_app())
    return _rest_api


