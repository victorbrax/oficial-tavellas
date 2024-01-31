import secrets
from datetime import datetime, timedelta

from flask_login import UserMixin

from database import db

from .. import SkeletonModel


class User(db.Model, UserMixin, SkeletonModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    image_path = db.Column(db.String(255))
    user_token = db.Column(db.String(255))
    token_expiration = db.Column(db.DateTime)
    roles = db.relationship("Role", secondary="role_user", backref=db.backref("user", lazy="dynamic"))

    def __init__(self, first_name, last_name, email, password, active):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.active = active
        self.user_token = None
        self.token_expiration = None
        self.image_path = f'https://ui-avatars.com/api/?name={self.first_name}+{self.last_name}&background=random'

    def gen_token(self):
        self.token_expiration = datetime.now() + timedelta(minutes=30)
        self.user_token = secrets.token_urlsafe(16)
        db.session.commit()
        return self.user_token
    
    def is_token_valid(self):
        return self.token_expiration is not None and datetime.now() < self.token_expiration
    
    def has_role(self, role):
        user_roles = [role.name for role in self.roles]
        if role in user_roles or "admin" in user_roles:
            return True
        return False

    def __repr__(self):
        return "<User %r>" % self.first_name
    
    def __str__(self):
        return self.first_name if len(f"{self.first_name} {self.last_name}") > 10 else f"{self.first_name} {self.last_name}"