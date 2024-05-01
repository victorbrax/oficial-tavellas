from app.models.auth.m_role import Role
from app.models.auth.m_user import User
from app import bcrypt

def create_dog_role():
    dog_role = Role.query.filter_by(name="dog").first()

    if not dog_role:
        dog = Role(name="dog", description="Super Ausuário")
        dog.save()

def create_thor_user():
    thor_user = User.query.filter_by(email="thor@tavellas.com.br").first()
    if not thor_user:
        super_thor = User(
            email="thor@tavellas.com.br",
            password = bcrypt.generate_password_hash("au1234au").decode("utf-8"),
            nome="Thor",
            sobrenome="Tavellas",
            ativo=True
        )
        super_role = Role.query.filter_by(name="dog").first()

        super_thor.roles.append(super_role)
        super_thor.save()