from app.models.admin.exemplares.m_author_books import authors_books
from database import db

from ... import SkeletonModel


class Author(db.Model, SkeletonModel):
    __tablename__ = "author"
    # __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', secondary=authors_books, backref=db.backref('author', lazy='dynamic'))

    def __init__(self, name, books):
        self.name = name
        self.books = books

    def to_dict(self):
        """Transforma todos os campos da tabela em um dicionário."""
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        model_dict['books'] = ", ".join([book.title for book in self.books])
        return model_dict

    @classmethod
    def is_createble(cls):
        return True

    @property
    def is_editable(self):
        return True

    @property
    def is_deletable(self):
        return True
    
    @property
    def is_reviewed(self):
        return True