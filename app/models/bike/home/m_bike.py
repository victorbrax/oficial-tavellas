from database import db

from ... import SkeletonModel
from app.models.cliente.home.m_cliente import Cliente

class Bike(db.Model, SkeletonModel):
    __tablename__ = "bike"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    condicao = db.Column(db.String(50), nullable=False)
    aro = db.Column(db.String(50), nullable=False)
    quadro = db.Column(db.Integer)
    cor = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', onupdate='CASCADE', ondelete="CASCADE"))

    servico = db.relationship('Servico', backref=db.backref('bike'), passive_deletes=True)


    def __init__(self, descricao, modelo, condicao, aro, quadro, cor, cliente):
        self.descricao = descricao
        self.modelo = modelo
        self.condicao = condicao
        self.aro = aro
        self.quadro = quadro
        self.cor = cor
        self.cliente = cliente
    
    def __repr__(self):
        return "<Bike %r>" % self.id
    
    def __str__(self):
        return f"{self.id}. {self.descricao}"
    
    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        model_dict['cliente'] = self.cliente.nome
        return model_dict

    def to_export_reports(self):
        report_dict = {}
        report_dict['id'] = self.id
        report_dict['cliente'] = self.cliente.nome
        report_dict["celular_cliente"] = self.cliente.celular
        report_dict['descricao'] = self.descricao
        report_dict['modelo'] = self.modelo
        report_dict['condicao'] = self.condicao
        report_dict['aro'] = self.aro
        report_dict['quadro'] = self.quadro
        report_dict['cor'] = self.cor
        report_dict['data_criacao'] = self.data_criacao
        return report_dict

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