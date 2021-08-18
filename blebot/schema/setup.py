from . import connection, Base
from .events import Event
from .stickies import Sticky
from .roles import Role

def create_database():
    db_engine = connection()
    Base.metadata.create_all(bind=db_engine)

def alter_table():
    db_engine = connection()
    db_engine.execute("DROP TABLE events")

if __name__ == "__main__":
    create_database()
