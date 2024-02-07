from database import db


class SkeletonModel:
    def __init__(self):
        pass

    @classmethod
    def verify_existing(cls, **primary_keys:dict) -> bool:
        """Retorna True se a consulta existir."""
        existing_item = db.session.query(cls).filter_by(**primary_keys).first()
        return existing_item is not None
    
    def to_dict(self):
        """Transforma todos os campos da tabela em um dicionário."""
        model_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        model_dict['is_editable'] = self.is_editable
        model_dict['is_deletable'] = self.is_deletable
        return model_dict

    def flush(self):
        db.session.flush()
        return True

    def edit(self):
        db.session.commit()
        return True

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @property
    def is_editable(self):
        # Lógica para permitir a edição do item em uma possível tabela.
        pass

    @property
    def is_deletable(self):
        # Lógica para permitir a edição do item em uma possível tabela.
        pass