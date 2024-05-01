from flask import flash, redirect, render_template, request, url_for

from app import bcrypt, db
from app.models.auth.m_user import User
from app.models.auth.m_role import Role
from app.models.auth.m_user_roles import role_user
from .f_accounts import RegistrationForm

from . import bp


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST" and form.validate():
        nome = form.nome.data
        sobrenome = form.sobrenome.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if not User.verify_existing(email=email):
            try:
                user = User(email=email, password=hashed_password, nome=nome, sobrenome=sobrenome, ativo=True)
                user_role = Role.query.get(1)
                user.roles.append(user_role)
                user.save()
                flash("Usuário registrado com sucesso.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                print(e)
                db.session.rollback()
                flash("Tente novamente, erro no banco de dados", "warning")
                print(e)
                return render_template("auth/accounts/v_register.html", form=form)
        else:
            flash("Inconsistência no ato do registro, verifique os dados.", "danger")

    return render_template("auth/accounts/v_register.html", form=form)
