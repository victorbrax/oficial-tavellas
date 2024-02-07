from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, validators, SubmitField
from wtforms.validators import InputRequired, Optional
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField

from app.models.cliente.home.m_cliente import Cliente
from app.models.reparo.home.m_reparo import Reparo
from app.models.bike.home.m_bike import Bike


class ServicoForms(FlaskForm):
    data_inicio = DateField('Data de Início', validators=[InputRequired()])
    data_fim = DateField('Data de Fim', validators=[Optional()])
    preco_total = DecimalField('Preço Total', validators=[Optional()])
   
    reparos = QuerySelectMultipleField('Reparo(s)', validators=[validators.DataRequired()]) # https://www.youtube.com/watch?v=d0jR-2UB9Y0
    cliente = QuerySelectField('Cliente', validators=[validators.DataRequired()], allow_blank=True)
    bike = QuerySelectField('Bike', validators=[validators.DataRequired()], allow_blank=True)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(ServicoForms, self).__init__(*args, **kwargs)
        self.reparos.query = Reparo.query.all()
        self.cliente.query = Cliente.query.all()
        self.bike.query = Bike.query.all()