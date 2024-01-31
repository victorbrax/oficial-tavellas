from flask_login import login_required

from . import bp


@bp.route("/xpto", methods=["GET", "POST"])
@login_required
def home2():
    return "xpto"