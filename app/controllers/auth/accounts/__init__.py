from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

from . import c_change, c_forgot, c_login, c_register
