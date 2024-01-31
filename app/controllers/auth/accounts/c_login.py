from flask import flash, g, redirect, render_template, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt, login_manager
from app.models.auth.m_user import User
from .f_accounts import LoginForm

from . import bp

login_manager.login_view = "auth.login"
login_manager.login_message = "Você precisa estar logado para visualizar essa página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    """Define como o Flask-Login carrega um usuário com base no ID armazenado no cookie de sessão.
    Internamente utilizado para carregar o objeto do usuário após autenticação, em todas as solicitações subsequentes."""
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash("Usuário logado com sucesso.", "success")
            return redirect(url_for("home.home"))
        else:
            flash("Inconsistência no ato do login.", "danger")
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))    
    return render_template("auth/accounts/v_login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    if session.get("logged_in"):
        session.pop("logged_in", None)
        flash("Usuário deslogado com sucesso.", "success")
    else:
        flash("Você não está logado.", "danger")
    logout_user()
    
    return redirect(url_for("auth.login"))