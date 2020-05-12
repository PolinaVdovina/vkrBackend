from config import DebugConfig as Config
from core import configure_app
from core import get_flask_app

configure_app(Config)
app = get_flask_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = Config.PORT)


