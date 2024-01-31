from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, StringField, SubmitField, validators)
from app.models.admin.exemplares.m_book import Book
from wtforms_alchemy import QuerySelectMultipleField

class AuthorForms(FlaskForm):
    name = StringField(validators=[validators.DataRequired()])
    books = QuerySelectMultipleField('Livros', validators=[validators.DataRequired()]) # https://www.youtube.com/watch?v=d0jR-2UB9Y0
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(AuthorForms, self).__init__(*args, **kwargs)
        # Realizar a consulta ao banco de dados dentro do contexto da aplicação (inicialização).
        self.books.query = Book.query.all()