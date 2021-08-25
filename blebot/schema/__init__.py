from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import database_exists

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'blerocks',
}

Base = declarative_base()

def connection(db_name):
    config = dict(DATABASE)
    config["database"] = db_name
    return create_engine(URL(**config))

def get_session(db_name):
    conn = connection(db_name)
    return sessionmaker(bind=conn)()

def create_database(db_name):
    url = "{driver}://{user}:{password}@{host}".format(
        driver=DATABASE["drivername"],
        user=DATABASE["username"],
        password=DATABASE["password"],
        host=DATABASE["host"]
    )

    if not database_exists(url):
        engine = create_engine(url)
        conn = engine.connect()
        conn.connection.set_isolation_level(0)
        try:
            conn.execute("CREATE DATABASE \"{name}\";".format(name=db_name))
        except ProgrammingError:
            pass
        conn.close()

    conn = connection(db_name)
    Base.metadata.create_all(bind=conn)
