from database import db

from ... import SkeletonModel


class Book(db.Model, SkeletonModel):
    __tablename__ = "book"
    __bind_key__ = "DEV"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, title):
        self.title = title

    def to_dict(self):
        """Transforma todos os campos da tabela em um dicionário."""
        model_dict = super().to_dict()
        model_dict['is_reviewed'] = self.is_reviewed
        model_dict['is_createble'] = self.is_createble
        return model_dict
    
    def __repr__(self):
        return "<Book %r>" % self.title
    
    def __str__(self):
        return self.title


    @property
    def is_createble(self):
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
    
