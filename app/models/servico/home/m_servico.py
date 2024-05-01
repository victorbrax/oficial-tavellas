from flask_login import current_user
from sqlalchemy.sql import func

from app.models.reparo.home.m_reparo import Reparo
from app.models.produto.home.m_produto import Produto
from app.models.relationships.t_reparo_servico import reparo_servico
from app.models.relationships.t_produto_servico import produto_servico
from database import db

from ... import SkeletonModel

possiveis_status = ["Aguardando Reparo", "Em Andamento", "Aguardando Pagamento", "Finalizado"]

class Servico(db.Model, SkeletonModel):
    __tablename__ = "servico"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    preco_total = db.Column(db.Numeric(10, 2))
    
    status  = db.Column(db.String(50))
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', onupdate='CASCADE', ondelete="CASCADE"))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id', onupdate='CASCADE', ondelete="CASCADE"))

    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    produtos = db.relationship('Produto', secondary=produto_servico, backref=db.backref('servico'), passive_deletes=True)
    reparos = db.relationship('Reparo', secondary=reparo_servico, backref=db.backref('servico'), passive_deletes=True)
    usuario = db.relationship('User', backref=db.backref('servico'))

    
    def __init__(self, cliente, data_inicio, data_fim, bike, reparos, produtos):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.reparos = reparos
        self.produtos = produtos
        self.cliente = cliente
        self.bike = bike
        self.usuario = current_user

    def update_status(self):
    
        if self.status is None: # Se o serviço estiver sendo criado, inicialize o status como o primeiro da lista
            self.status = possiveis_status[0]
            db.session.commit()
        else:
            current_status_index = possiveis_status.index(self.status)

            # Se o status atual não for o último da lista, atualize para o próximo
            if current_status_index < len(possiveis_status) - 1:
                self.status = possiveis_status[current_status_index + 1]

            if current_status_index == 2:
                self.data_fim = db.func.current_date()



    def update_preco_total(self):
        total_reparos = 0
        total_servicos = 0

        if self.reparos:    
            total_reparos = db.session.query(func.coalesce(func.sum(Reparo.preco), 0)).filter(Reparo.id.in_([reparo.id for reparo in self.reparos])).scalar()

        if self.produtos:
            total_servicos = db.session.query(func.coalesce(func.sum(Produto.preco), 0)).filter(Produto.id.in_([produto.id for produto in self.produtos])).scalar()

        self.preco_total = total_reparos + total_servicos


    def to_dict(self):
        model_dict = super().to_dict()
        model_dict['is_updatable'] = self.is_updatable
        model_dict['reparos'] = ", ".join([reparo.nome for reparo in self.reparos])
        model_dict['produtos'] = ", ".join([produto.nome for produto in self.produtos])
        model_dict['cliente'] = f"{self.cliente.id}. {self.cliente.nome}"
        model_dict['bike'] = self.bike.descricao
        model_dict['usuario'] = f"{self.usuario.nome} {self.usuario.sobrenome}"
        return model_dict
    
    def to_export_reports(self):
        export_dict = {}
        export_dict["id_servico"] = self.id
        export_dict["descricao_bike"] = self.bike.descricao
        export_dict["modelo_bike"] = self.bike.modelo
        export_dict["status"] = self.status
        export_dict["reparos"] = ", ".join([reparo.nome for reparo in self.reparos])
        export_dict["observacao"] = self.bike.condicao
        export_dict["responsavel"] = f"{self.usuario.nome} {self.usuario.sobrenome}"
        export_dict["email_responsavel"] = self.usuario.email
        export_dict["celular_responsavel"] = "19 99287-1844"
        export_dict["data_inicio"] = self.data_inicio
        export_dict["data_fim"] = self.data_fim
        export_dict["celular_cliente"] = self.cliente.celular
        return export_dict
    
    def to_export_xls(self):
        export_dict = {}
        export_dict["id_servico"] = self.id
        export_dict["descricao_bike"] = self.bike.descricao
        export_dict["modelo_bike"] = self.bike.modelo
        export_dict["status"] = self.status
        export_dict["reparos"] = ", ".join([reparo.nome for reparo in self.reparos])
        export_dict["observacao"] = self.bike.condicao
        export_dict["responsavel"] = f"{self.usuario.nome} {self.usuario.sobrenome}"
        export_dict["email_responsavel"] = self.usuario.email
        export_dict["celular_responsavel"] = "19 99287-1844"
        export_dict["data_inicio"] = self.data_inicio
        export_dict["data_fim"] = self.data_fim
        export_dict["celular_cliente"] = self.cliente.celular
        return export_dict

    @classmethod
    def is_createble(cls):
        return True

    @classmethod
    def is_exportable(cls):
        return True

    @property
    def is_editable(self):
        return True

    @property
    def is_deletable(self):
        return True
    
    @property
    def is_updatable(self):
        if self.status == possiveis_status[-1]:
            return False
        return True