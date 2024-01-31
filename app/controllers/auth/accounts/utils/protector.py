from functools import wraps

from flask import abort, flash
from flask_login import current_user


def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.active:
                user_roles = [role.name for role in current_user.roles]
                if any(role in user_roles for role in required_roles) or "admin" in user_roles:
                    return func(*args, **kwargs)
                else:
                    flash("Você não tem permissão para acessar esta página.", "danger")
                    return abort(403)
            else:
                flash("Você não tem permissão para acessar esta página.", "danger")
                return abort(403)
        return wrapper
    return decorator