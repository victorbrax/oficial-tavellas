from database import db


class Produto(db.Model):
    __tablename__ = "produto"
    __table_args__ = {"schema": "portal"}

    id = db.Column(db.Integer, primary_key=True)
    codigobarras = db.Column(db.String())
    descricaoproduto = db.Column(db.String())
    idutilizacaoproduto = db.Column(db.Integer)
    idsituacaoproduto = db.Column(db.Integer)
    exclusivoecommerce = db.Column(db.String())
    idprincipalmaster = db.Column(db.Integer)
    idsubcodigoproduto = db.Column(db.Integer)
    subcodigo = db.Column(db.String())
    descricaosubcodigo = db.Column(db.String())
    idsubgrupoproduto = db.Column(db.Integer)
    descricaosubgrupoproduto = db.Column(db.String())
    idgrupoproduto = db.Column(db.Integer)
    descricaogrupoproduto = db.Column(db.String())
    idsetorproduto = db.Column(db.Integer)
    descricaosetorproduto = db.Column(db.String())
    iddepartamento = db.Column(db.Integer)
    descricaodepartamento = db.Column(db.String())
    idsegmentoproduto = db.Column(db.Integer)
    descricaosegmentoproduto = db.Column(db.String())
    
    def verify_existing(self, **primary_keys:dict) -> bool:
        """Retorna True se a consulta existir."""
        existing_item = db.session.query(self.__class__).filter_by(**primary_keys).first()
        return existing_item is None

    @classmethod
    def get_products_by_setors(cls, setor_ids):
        produtos = db.session.query(cls.id, cls.codigobarras, cls.descricaoproduto)\
                        .filter(cls.idsetorproduto.in_(setor_ids))\
                        .all()

        return [ {"id":p.id, "codigobarras":p.codigobarras, "descricao":p.descricaoproduto.replace("'","").replace('"',"") } for p in produtos ]
