from flask import flash, redirect, render_template, request, url_for
from flask_mail import Message

from app import bcrypt, mail
from app.models.auth.m_user import User
from .f_accounts import ForgotForm, ForgotResetForm

from . import bp


@bp.route("/forgot", methods=["GET", "POST"])
def forgot():
    form = ForgotForm()

    if request.method == "POST" and form.validate():
        email = form.email.data
        
        if User.verify_existing(email=email):
            user = User.query.filter_by(email=email).first()

            flash("Um e-mail com o Token de recuperação foi enviado.", "success")
            user_token = user.gen_token()
            reset_link = url_for('auth.forgot_reset', token=user_token, _external=True)

            msg = Message()
            msg.subject = "Validação de Troca de Senha - [Sitema Tavella's]"
            msg.recipients = [user.email]
            msg.html = render_template("auth/accounts/email/forgot_mail.html", reset_link=reset_link)
            mail.send(msg)
            return redirect(url_for("auth.login"))

        else:
            flash("E-mail não encontrado. Verifique os dados e tente novamente.", "danger")
    return render_template("auth/accounts/v_forgot.html", form=form)


@bp.route("/forgot/<token>", methods=["GET", "POST"])
def forgot_reset(token):

    form = ForgotResetForm()
    if User.verify_existing(user_token=token):
        user = User.query.filter_by(user_token=token).first()

        if user.is_token_valid():

            if request.method == "POST" and form.validate():
                password = form.data["password"]
                hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
                user.password = hashed_password
                user.user_token = None
                user.token_expiration = None
                user.edit()
                flash("Senha alterada com sucesso.", "success")
                return redirect(url_for("auth.login"))
        else:
            flash("Token inválido, tente gerar um novo.", "danger")

    else:
        flash("Inconsistência nos dados, verifique.", "danger")
        
    return render_template("auth/accounts/v_forgot_token.html", form=form, token=token)
