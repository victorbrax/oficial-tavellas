from flask import Blueprint

bp = Blueprint("bike", __name__, url_prefix="/bike")
from . import c_bike_view