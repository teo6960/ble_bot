from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'blerocks',
    'database': 'mydb'
}

Base = declarative_base()

def connection():
    return create_engine(URL(**DATABASE))

def get_session():
    conn = connection()
    return sessionmaker(bind=conn)()
