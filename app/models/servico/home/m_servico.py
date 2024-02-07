from flask_login import current_user
from sqlalchemy.sql import func

from app.models.reparo.home.m_reparo import Reparo
from app.models.relationships.t_reparo_servico import reparo_servico
from database import db

from ... import SkeletonModel


class Servico(db.Model, SkeletonModel):
    __tablename__ = "servico"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime)
    data_fim = db.Column(db.DateTime)
    preco_total = db.Column(db.Numeric(10, 2))
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    reparos = db.relationship('Reparo', secondary=reparo_servico, backref=db.backref('servico', lazy='dynamic'))
    cliente = db.relationship('Cliente', backref=db.backref('servico'))
    bike = db.relationship('Bike', backref=db.backref('servico'))
    usuario = db.relationship('User', backref=db.backref('servico'))

    def __init__(self, data_inicio, data_fim, reparos, cliente, bike):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.reparos = reparos
        self.cliente = cliente
        self.bike = bike
        self.usuario = current_user

    def update_preco_total(self):
            if self.reparos:
                total_reparos = db.session.query(func.coalesce(func.sum(Reparo.preco), 0)).filter(Reparo.id.in_([reparo.id for reparo in self.reparos])).scalar()
                self.preco_total = total_reparos
            else:
                self.preco_total = 0

    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        model_dict['reparos'] = ", ".join([reparo.nome for reparo in self.reparos])
        model_dict['cliente'] = self.cliente.nome
        model_dict['bike'] = self.bike.modelo
        model_dict['usuario'] = f"{self.usuario.first_name} {self.usuario.last_name}"
        return model_dict
    
    def extra_dict(self): # child rows
        kronik = {}
        kronik['meu_pau'] ="fator_crucial"
        return kronik 

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