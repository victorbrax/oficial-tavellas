from flask import Blueprint

bp = Blueprint("reparo", __name__, url_prefix="/reparo")
from . import c_reparo_view