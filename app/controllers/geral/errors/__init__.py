from flask import Blueprint

bp = Blueprint("errors", __name__)
from . import c_errors_handlers
