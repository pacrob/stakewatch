from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Provider_Data(Base):
    __tablename__ = "provider_data"
    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    staker_name = Column(String)
    chain_id = Column(Integer)
    latest_block_number = Column(Integer)
    latest_block_from_truth = Column(Integer)

# from sqlalchemy import create_engine
# engine = create_engine('sqlite:////db/stakewatch.db'

import sqlalchemy as db

def connect_to_db():
    engine = db.create_engine('sqlite:////db/stakewatch.db')
    connection = engine.connect()
    metadata = db.MetaData()
    table = Table('stakewatch', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('url', String),
                           Column('nickname', String),
                           Column('connected', String),
                           Column('chain_id', Integer, default=None),
                           Column('latest_block', Integer, default=None),
                           Column('time_stamp', DateTime),
                       )
    
    metadata.create_all(engine)

    return table, connection, metadata
    

def write_to_db(table, connection, metadata, data):
    query = db.insert(table)
    ResultProxy = connection.execute(query, data)
