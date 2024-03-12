from database import db

from ... import SkeletonModel


class Produto(db.Model, SkeletonModel):
    __tablename__ = "produto"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    marca = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Numeric(precision=10, scale=2))
    local = db.Column(db.Integer)

    def __init__(self, nome, preco, marca, local):
        self.nome = nome
        self.marca = marca
        self.preco = preco
        self.local = local

    def __repr__(self):
        return "<Produto %r>" % self.id
    
    def __str__(self):
        return f"{self.id}. {self.nome}"

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