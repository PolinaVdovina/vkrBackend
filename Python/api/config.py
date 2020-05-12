class Config(object):
    JWT_SECRET_KEY = 'super_secret_troll_key'
    SECRET_KEY = 'super_secret_troll_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123qweasdZXC@localhost:5432/how_to_build'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    PORT = 5000
    # UPLOAD_FOLDER = 'C:/Users/DiamondDog/Documents/Projects/HowToStudy/Python/api/static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'diamonddog1234'
    MAIL_PASSWORD = '123qweasdZXC'
    BOT_PASSWORD = "1488"
    # administrator list
    ADMINS = ['diamonddog1234@gmail.com']
    MAIL_DEFAULT_SENDER = 'diamonddog1234@gmail.com'


class DebugConfig(Config):
    DEBUG = True
