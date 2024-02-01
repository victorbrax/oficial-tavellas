from flask import Blueprint

bp = Blueprint("cliente", __name__, url_prefix="/cliente")
from . import c_cliente_view