from database import db


produto_servico = db.Table('produto_servico',
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id', onupdate='CASCADE', ondelete="CASCADE"), primary_key=True),
    db.Column('servico_id', db.Integer, db.ForeignKey('servico.id', onupdate='CASCADE', ondelete="CASCADE"), primary_key=True),
    # bind_key="DEV"
)