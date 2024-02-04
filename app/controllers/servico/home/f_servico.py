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
    reparos = QuerySelectMultipleField('Reparos(s)', validators=[validators.DataRequired()]) # https://www.youtube.com/watch?v=d0jR-2UB9Y0

    cliente_id = QuerySelectField('Cartão do Cliente', validators=[InputRequired()])
    bike_id = QuerySelectField('Bicicleta', validators=[InputRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(ServicoForms, self).__init__(*args, **kwargs)
        # Realizar a consulta ao banco de dados dentro do contexto da aplicação (inicialização).
        self.cliente_id.query = Cliente.query.all()
        self.bike_id.query = Bike.query.all()
        self.reparos.query = Reparo.query.all()

        # self.bike_id.query = Bike.query.filter_by(cliente_id=self.cliente_id.data).all()
