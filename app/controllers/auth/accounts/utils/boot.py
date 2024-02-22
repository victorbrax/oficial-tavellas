from app.models.auth.m_role import Role
from app.models.auth.m_user import User
from app import bcrypt

def create_god_role():
    god_role = Role.query.filter_by(name="god").first()

    if not god_role:
        god = Role(name="god", description="Super Ausuário")
        god.save()

def create_thor_user():
    thor_user = User.query.filter_by(email="thor@tavellas.com.br").first()
    if not thor_user:
        super_thor = User(
            email="thor@tavellas.com.br",
            password = bcrypt.generate_password_hash("au1234au").decode("utf-8"),
            first_name="Thor",
            last_name="Tavellas",
            active=True
        )
        super_role = Role.query.filter_by(name="god").first()

        super_thor.roles.append(super_role)
        super_thor.save()