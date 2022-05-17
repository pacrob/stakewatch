from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import sqlalchemy as db

def connect_to_db():
    engine = db.create_engine('sqlite:////db/stakewatch.db')
    connection = engine.connect()
    metadata = db.MetaData()
    table = Table('stakewatch', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('providers_blob', String(2048)),
                       )
    
    metadata.create_all(engine)

    return table, connection, metadata
    

def write_to_db(table, connection, metadata, data):
    # print(f'TABLE {table}, TYPE_OF_DATA {type(data)}, DATA {data}', flush=True)
    query = db.insert(table)
    ResultProxy = connection.execute(query, data)
    # ResultProxy = connection.execute(query, 'cats')

