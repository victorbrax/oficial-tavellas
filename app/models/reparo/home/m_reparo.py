from database import db

from ... import SkeletonModel


class Reparo(db.Model, SkeletonModel):
    __tablename__ = "reparo"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Numeric(precision=10, scale=2))
    qtd_horas = db.Column(db.Integer)

    def __init__(self, nome, preco, qtd_horas):
        self.nome = nome
        self.preco = preco
        self.qtd_horas = qtd_horas

    def __repr__(self):
        return "<Reparo %r>" % self.id
    
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