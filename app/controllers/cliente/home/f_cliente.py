from flask_wtf import FlaskForm
from wtforms import (EmailField, TelField, StringField, SubmitField, validators)


class ClienteForms(FlaskForm):
    nome = StringField(validators=[validators.DataRequired()])
    celular = TelField(validators=[validators.DataRequired()])
    telefone = TelField(validators=[validators.DataRequired()])
    email = EmailField(validators=[validators.DataRequired()])
    cep = StringField(validators=[validators.DataRequired()])
    rua = StringField(validators=[validators.DataRequired()])
    bairro = StringField(validators=[validators.DataRequired()])
    complemento = StringField()
    numero = StringField(validators=[validators.DataRequired()])
    cidade = StringField(validators=[validators.DataRequired()])
    estado = StringField(validators=[validators.DataRequired()])
    submit = SubmitField()