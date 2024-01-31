from database import db
from flask_login import current_user

from ... import SkeletonModel


class Uzuario(db.Model, SkeletonModel):
    __tablename__ = "uzuario"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def __init__(self, name, age, address, phone, email):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email

    def to_dict(self):
        """Transforma todos os campos da tabela em um dicionário."""
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        return model_dict
    
    def __repr__(self):
        return "<Uzuario %r>" % self.name
    
    def __str__(self):
        return self.name

    @classmethod
    def is_createble(cls):
        return True

    @property
    def is_editable(self):
        if "covabra" in current_user.email:
            return True

    @property
    def is_deletable(self):
        return True
    
    @property
    def is_reviewed(self):
        return True
    
