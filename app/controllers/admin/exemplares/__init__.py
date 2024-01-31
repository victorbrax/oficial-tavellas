from flask import Blueprint

bp = Blueprint("exemplo", __name__, url_prefix="/admin/exemplares")
from . import c_example_uzuario
from . import c_example_author