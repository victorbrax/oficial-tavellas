# CODING: UTF8
# CIC PORTAL
from dotenv import find_dotenv, load_dotenv
import json
import os

env = find_dotenv()
load_dotenv(env)

# PATHS
PORTAL_PATH = os.getcwd()
APP_PATH = os.path.join(PORTAL_PATH, "app")
MODELS_PATH = os.path.join(APP_PATH, "models")
VIEWS_PATH = os.path.join(APP_PATH, "views")
CONTROLLERS_PATH = os.path.join(APP_PATH, "controllers")
STATIC_PATH = os.path.join(APP_PATH, "public")

CIC_ENV = os.getenv("CIC_SETTINGS")
ERP_ENV = os.getenv("ERP_SETTINGS")
VENDA_ENV = os.getenv("VENDA_SETTINGS")

try:
    DB_CIC = json.loads(CIC_ENV)
    DB_ERP = json.loads(ERP_ENV)
    DB_VENDA = json.loads(VENDA_ENV)
except:
    DB_CIC = {}
    DB_ERP = {}
    DB_VENDA = {}
    print("Não foi possível autenticar-se aos bancos de dados PostgreSQL.")

class Config(object):
    SECRET_KEY = "c219d4e3-3ea8-4dbb-8641-C1C-P0RT4L-3ea8-4dbb-8641-8bbfc644aa18"
    CSRF_ENABLED = True

    MAIL_SERVER = "smtp.emailexchangeonline.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = "cic@covabra.com.br"
    MAIL_USERNAME = "cic@covabra.com.br"
    MAIL_PASSWORD = "2yNDhV&P"

    SQLALCHEMY_DATABASE_URI = "sqlite:///production.sqlite"
    SQLALCHEMY_BINDS = {
        "DEV": "sqlite:///development.sqlite"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'Slate' # https://bootswatch.com/3/


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True

class ProductionConfig(Config):
    if DB_CIC:
        FLASK_ENV = "production"