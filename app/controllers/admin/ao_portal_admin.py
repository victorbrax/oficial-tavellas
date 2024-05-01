from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

from app import bcrypt


# Fazer com que o Menu de Index tenha um botão para voltar para a Home
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("home.home")

# Flask Admin Views
class ControlAdminView(AdminIndexView): # Herança de AdminIndexView para permitir validação de autenticação.

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

class UserView(ModelView):
    column_hide_backrefs = False
    column_list = ("nome", "sobrenome", "email", "ativo", "roles")
    column_searchable_list = ["nome", "sobrenome", "email"]
    column_editable_list = ["nome", "sobrenome", "email", "roles", "ativo", "imagem_url"]
    column_filters = ["roles"]
    form_columns = ["nome", "sobrenome", "email", "password", "ativo", "imagem_url", "roles"]

    def on_model_change(self, form, model, is_created):
        if hasattr(form, 'password') and form.password.data:
            if not form.password.data.startswith("$2b$"): # Se não começar com "$2b$", então assumimos que não é um hash bcrypt
                model.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    def on_form_prefill(self, form, id):
        if not form.imagem_url.data:
            form.imagem_url.data = f'https://ui-avatars.com/api/?name={form.nome.data}+{form.sobrenome.data}&background=random'

class RoleView(ModelView):
    form_excluded_columns = ["user"]