from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

from app import bcrypt


class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("home.home")

# Flask Admin Views
class ControlAdminView(AdminIndexView): # Herança de AdminIndexView para permitir validação de autenticação.

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

class UserView(ModelView):
    column_hide_backrefs = False
    column_list = ("first_name", "last_name", "email", "active", "roles")
    column_searchable_list = ["first_name", "last_name", "email"]
    column_editable_list = ["first_name", "last_name", "email", "roles", "active", "image_path"]
    column_filters = ["roles"]
    form_columns = ["first_name", "last_name", "email", "password", "active", "image_path", "roles"]

    def on_model_change(self, form, model, is_created):
        if hasattr(form, 'password') and form.password.data:
            if not form.password.data.startswith("$2b$"): # Se não começar com "$2b$", então assumimos que não é um hash bcrypt
                model.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    def on_form_prefill(self, form, id):
        if not form.image_path.data:
            form.image_path.data = f'https://ui-avatars.com/api/?name={form.first_name.data}+{form.last_name.data}&background=random'

class RoleView(ModelView):
    form_excluded_columns = ["user"]