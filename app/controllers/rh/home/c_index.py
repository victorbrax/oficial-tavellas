from flask import render_template
from flask_login import login_required

from app import db
from app.controllers.auth.accounts.utils.protector import role_required

from . import bp


@bp.route("/", methods=["GET", "POST"])
@login_required
@role_required(["rh"])
def home():
    return render_template("rh/home/v_cards.html")

