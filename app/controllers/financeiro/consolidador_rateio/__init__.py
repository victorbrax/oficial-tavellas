from flask import Blueprint

bp = Blueprint("consolidador_rateio", __name__, url_prefix="/financeiro")
from . import c_consolidador_rateio
