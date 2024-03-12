from database import db

from .. import SkeletonModel


class Role(db.Model, SkeletonModel):
    __tablename__ = "role"
    # __bind_key__ = "DEV"

    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Role %r>" % self.name
    
    def __str__(self):
        return self.name