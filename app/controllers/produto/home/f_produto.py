from flask_wtf import FlaskForm
from wtforms import (DecimalField, StringField, SubmitField, validators)


class ProdutoForms(FlaskForm):
    nome = StringField(validators=[validators.DataRequired()])
    preco = DecimalField(validators=[validators.DataRequired()])
    marca = StringField(validators=[validators.DataRequired()])
    local = StringField(validators=[validators.DataRequired()])
    submit = SubmitField()