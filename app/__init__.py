from importlib import import_module

from flask import Flask, g
from flask_admin import Admin
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


from app.models.auth.m_user import User
from app.models.auth.m_role import Role
from app.models.auth.m_user_roles import role_user

from app.models.admin.exemplares.m_author import Author
from app.models.admin.exemplares.m_book import Book
from app.models.admin.exemplares.m_author_books import authors_books

from app.models.produto.home.m_produto import Produto
from app.models.reparo.home.m_reparo import Reparo

from config import ProductionConfig
from database import db

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
babel = Babel()
mail = Mail()
admin = Admin(name="Controle CIC", template_mode="bootstrap3")

def get_locale():
    return 'pt_BR'

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="public")
    app.config.from_object(ProductionConfig)

    from .controllers.auth.accounts.utils.boot import create_dog_role, create_thor_user

    # Flask Admin Views
    from .controllers.admin.ao_portal_admin import (ControlAdminView, MainIndexLink, RoleView, UserView)
    admin.add_link(MainIndexLink(name="Home"))
    admin.add_view(UserView(User, db.session, url="usuarios", endpoint="users"))
    admin.add_view(RoleView(Role, db.session, url="cargos", endpoint="roles"))
    
    blueprints_to_import = [
        "home.inicio",
        "admin.exemplares",
        "admin.backup",
        "auth.accounts",
        "geral.errors",
        "bike.home", # Home
        "bike.api", # API
        "produto.home", # Home
        "cliente.home", # Home
        "reparo.home", # Home
        "servico.home", # Home
        "financeiro.home", # Home
        "financeiro.consolidador_rateio", # Departamento App
    ]

    for blueprint_name in blueprints_to_import:
        module = import_module(f".controllers.{blueprint_name}", __name__)
        blueprint = getattr(module, "bp")
        app.register_blueprint(blueprint)

    # Extensions Init
    babel.init_app(app=app, locale_selector=get_locale)
    admin.init_app(app=app, index_view=ControlAdminView())
    db.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app=app)
    bcrypt.init_app(app=app)

    with app.app_context(): #! It is important that you import your models after initializing the db object since.
        db.create_all()
        create_dog_role()
        create_thor_user()
    return app