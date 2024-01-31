from flask import render_template

from . import bp


# 404 Page not found error default handler
@bp.app_errorhandler(404)
def handle404(error):
    return render_template("geral/errors/404.html")

# 403 Forbidden
@bp.app_errorhandler(403)
def handle404(error):
    return render_template("geral/errors/403.html")