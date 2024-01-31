from sqlalchemy.ext.automap import automap_base
import sqlalchemy as sa
from sqlalchemy import text
from . import db

def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    """Deals with a naming conflict problem."""
    name = referred_cls.__name__.lower()
    local_table = local_cls.__table__
    if name in local_table.columns:
        newname = name + "_"
        return newname
    return name

def get_db_engine(bind_key):
    if bind_key is None:
        engine = db.engine
    else:
        engine = db.get_engine(bind=bind_key, charset='utf8')
    return engine

def get_model(engine, table_name, schema):
    metadata = sa.MetaData()
    metadata.reflect(engine, schema=schema, only=[table_name])    
    Base = automap_base(metadata=metadata)
    Base.prepare(name_for_scalar_relationship=name_for_scalar_relationship)
    Model = Base.classes[table_name]
    return Model

def execute_query_from_file(file_path, bind_key=None, parameters=None):
    engine = get_db_engine(bind_key)
    connection = engine.connect()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql = file.read()
        if parameters:
            sql = sql.format(**parameters)
        query = text(sql)
        result = connection.execute(query)
        rows = result.fetchall()
        output = [tuple(row) for row in rows]
        return output
    finally:
        connection.close()