from app.models.auth.m_user_roles import role_user
import secrets
from datetime import datetime, timedelta

from flask_login import UserMixin

from database import db

from .. import SkeletonModel


class User(db.Model, UserMixin, SkeletonModel):
    __tablename__ = "user"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    sobrenome = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    ativo = db.Column(db.Boolean())
    imagem_url = db.Column(db.String(255))
    user_token = db.Column(db.String(255))
    token_expiration = db.Column(db.DateTime)
    roles = db.relationship("Role", secondary=role_user, backref=db.backref("user", lazy="dynamic"))

    def __init__(self, nome, sobrenome, email, password, ativo):
        self.nome = nome
        self.sobrenome = sobrenome
        self.password = password
        self.email = email
        self.ativo = ativo
        self.user_token = None
        self.token_expiration = None
        self.imagem_url = f'https://ui-avatars.com/api/?name={self.nome}+{self.sobrenome}&background=random'

    def gen_token(self):
        self.token_expiration = datetime.now() + timedelta(minutes=30)
        self.user_token = secrets.token_urlsafe(16)
        db.session.commit()
        return self.user_token
    
    def is_token_valid(self):
        return self.token_expiration is not None and datetime.now() < self.token_expiration
    
    def has_role(self, role):
        user_roles = [role.name for role in self.roles]
        if role in user_roles or "Admin" in user_roles or "dog" in user_roles:
            return True
        return False

    def __repr__(self):
        return "<User %r>" % self.nome
    
    def __str__(self):
        return self.nome if len(f"{self.nome} {self.sobrenome}") > 12 else f"{self.nome} {self.sobrenome}"