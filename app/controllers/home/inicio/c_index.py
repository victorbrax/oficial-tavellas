from flask import render_template
from flask_login import login_required

from . import bp


@bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home/inicio/v_index.html")