from flask import Blueprint

bp = Blueprint("rh", __name__, url_prefix="/rh")
from . import c_index
