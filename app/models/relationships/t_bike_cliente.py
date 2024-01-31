from database import db


bike_cliente = db.Table('bike_cliente',
    db.Column('bike_id', db.Integer, db.ForeignKey('bike.id'), primary_key=True),
    db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id'), primary_key=True),
    bind_key="DEV"
)