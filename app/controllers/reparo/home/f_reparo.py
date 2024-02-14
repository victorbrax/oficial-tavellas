from flask_wtf import FlaskForm
from wtforms import (DecimalField, IntegerField, StringField, SubmitField, validators)


class ReparoForms(FlaskForm):
    nome = StringField(validators=[validators.DataRequired()])
    preco = DecimalField(validators=[validators.DataRequired()])
    qtd_horas = IntegerField(validators=[validators.DataRequired()])
    submit = SubmitField()