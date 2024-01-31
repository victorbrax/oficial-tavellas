from flask import Blueprint

bp = Blueprint("bike", __name__, url_prefix="/bike")
from . import c_bikes_view