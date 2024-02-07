from flask import Blueprint

bp = Blueprint("bike_api", __name__, url_prefix="/api/bike")
from . import c_bike_utils