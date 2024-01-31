# from app.models.admin.exemplares.m_author_books import authors_books
from database import db

from ... import SkeletonModel


class Cliente(db.Model, SkeletonModel):
    __tablename__ = "cliente"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    celular = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, celular, telefone):
        self.nome = nome
        self.celular = celular
        self.telefone = telefone

    def __repr__(self):
        return "<Cliente %r>" % self.id
    
    def __str__(self):
        return self.nome

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        return model_dict

    @classmethod
    def is_createble(cls):
        return True

    @property
    def is_editable(self):
        return True

    @property
    def is_deletable(self):
        return True
    
    @property
    def is_reviewed(self):
        return True