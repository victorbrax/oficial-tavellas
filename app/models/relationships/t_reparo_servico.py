from database import db


reparo_servico = db.Table('reparo_servico',
    db.Column('reparo_id', db.Integer, db.ForeignKey('reparo.id', onupdate='CASCADE', ondelete="CASCADE"), primary_key=True),
    db.Column('servico_id', db.Integer, db.ForeignKey('servico.id', onupdate='CASCADE', ondelete="CASCADE"), primary_key=True),
    # bind_key="DEV"
)