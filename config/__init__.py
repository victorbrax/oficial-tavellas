from dotenv import find_dotenv, load_dotenv
import os

env = find_dotenv()
load_dotenv(env)

# Define o diretório base do aplicativo Flask
base_dir = os.getcwd()
APP_PATH = os.path.join(base_dir, "app")
DATABASE_PATH = os.path.join(base_dir, "database")
BACKUP_PATH = os.path.join(DATABASE_PATH, "backup")
MODELS_PATH = os.path.join(APP_PATH, "models")
VIEWS_PATH = os.path.join(APP_PATH, "views")
CONTROLLERS_PATH = os.path.join(APP_PATH, "controllers")
STATIC_PATH = os.path.join(APP_PATH, "public")
REPORT_PATH = os.path.join(STATIC_PATH, "report")

class Config(object):
    SECRET_KEY = "c219d4e3-3ea8-4dbb-8641-T4V32LL4S-P0RT4L-3ea8-4dbb-8641-8bbfc644aa18"
    CSRF_ENABLED = True

    MAIL_SERVER = "smtp.emailexchangeonline.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = "joaogomespcl@gmail.com" # Alterar para credenciais do aplicativo.
    MAIL_USERNAME = "joaogomespcl@gmail.com"
    MAIL_PASSWORD = "2yNDhV&P"
    
    DB_NAME = "tavellasprod.sqlite"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATABASE_PATH, DB_NAME)

#     @app.before_first_request
# def before_first_request():
#     with app.app_context():
#         db.engine.execute('pragma foreign_keys=on')
    
    SQLALCHEMY_BINDS = {
        "DEV": 'sqlite:///' + os.path.join(DATABASE_PATH, 'development.sqlite')
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'Slate' # https://bootswatch.com/3/


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True

class ProductionConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    # FLASK_ENV = "production"
