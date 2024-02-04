from app.models.relationships.t_reparo_servico import reparo_servico
from flask_login import current_user
from database import db

from ... import SkeletonModel


class Servico(db.Model, SkeletonModel):
    __tablename__ = "servico"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    data_incio = db.Column(db.DateTime)
    data_fim = db.Column(db.DateTime)
    preco_total = db.Column(db.Numeric(10, 2))
    reparos = db.relationship('Reparo', secondary=reparo_servico, backref=db.backref('bike', lazy='dynamic'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, data_inicio, data_fim, preco_total, reparos, cliente_id, bike_id):
        self.data_incio = data_inicio
        self.data_fim = data_fim
        self.preco_total = preco_total
        self.reparos = reparos
        self.cliente_id = cliente_id
        self.bike_id = bike_id
        self.usuario_id = current_user

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        model_dict['reparos'] = ", ".join([reparo.nome for reparo in self.reparos])
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