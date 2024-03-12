from flask import Blueprint

bp = Blueprint("backup", __name__, url_prefix="/admin/backup")
from . import c_backup_view