from flask_wtf import FlaskForm
from wtforms import (IntegerField, StringField, SubmitField, validators)
from app.models.cliente.home.m_cliente import Cliente
from wtforms_alchemy import QuerySelectField

class BikeForms(FlaskForm):
    descricao = StringField(validators=[validators.DataRequired()])
    modelo = StringField(validators=[validators.DataRequired()])
    condicao = StringField(validators=[validators.DataRequired()])
    aro = IntegerField(validators=[validators.DataRequired()])
    quadro = StringField(validators=[validators.DataRequired()])
    cor = StringField(validators=[validators.DataRequired()])
    cliente = QuerySelectField('Dono') # https://www.youtube.com/watch?v=d0jR-2UB9Y0
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(BikeForms, self).__init__(*args, **kwargs)
        # Realizar a consulta ao banco de dados dentro do contexto da aplicação (inicialização).
        self.cliente.query = Cliente.query.all()