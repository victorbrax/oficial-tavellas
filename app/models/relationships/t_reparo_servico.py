from database import db


reparo_servico = db.Table('reparo_servico',
    db.Column('reparo_id', db.Integer, db.ForeignKey('reparo.id'), primary_key=True),
    db.Column('servico_id', db.Integer, db.ForeignKey('servico.id'), primary_key=True),
    bind_key="DEV"
)