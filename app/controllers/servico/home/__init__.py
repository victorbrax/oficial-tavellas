from flask import Blueprint

bp = Blueprint("servico", __name__, url_prefix="/servico")
from . import c_servico_view