from flask import Blueprint

bp = Blueprint("produto", __name__, url_prefix="/produto")
from . import c_produto_view