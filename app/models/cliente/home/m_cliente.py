from database import db

from ... import SkeletonModel


class Cliente(db.Model, SkeletonModel):
    __tablename__ = "cliente"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    celular = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.Integer)
    rua = db.Column(db.String(150))
    bairro  = db.Column(db.String(80))
    numero = db.Column(db.Integer)
    complemento = db.Column(db.String(256))
    cidade = db.Column(db.String(40))
    estado = db.Column(db.String(30))

    bike = db.relationship('Bike', backref=db.backref('cliente'), passive_deletes=True)
    servico = db.relationship('Servico', backref=db.backref('cliente'), passive_deletes=True)

    def __init__(self, nome, celular, telefone, email, cep,  rua, bairro, numero, cidade, estado):
        self.nome = nome
        self.celular = celular
        self.telefone = telefone
        self.email = email
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.cidade = cidade
        self.estado = estado


    def __repr__(self):
        return "<Cliente %r>" % self.id
    
    def __str__(self):
        return f"{self.id}. {self.nome}"

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