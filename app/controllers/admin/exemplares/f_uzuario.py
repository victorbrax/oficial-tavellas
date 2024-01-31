from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, StringField, SubmitField, validators)


class UzuarioForms(FlaskForm):
    name = StringField(validators=[validators.DataRequired()])
    age = IntegerField(validators=[validators.DataRequired()])
    phone = IntegerField(validators=[validators.DataRequired()])
    address = StringField(validators=[validators.DataRequired()])
    email = EmailField(validators=[validators.DataRequired()])
    submit = SubmitField()