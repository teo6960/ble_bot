from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from . import ArraySet
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

import datetime

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'blerocks',
    'database': 'mydb'
}

class Event(Base):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    created_by = Column("created_by", String)
    going = Column("going", ArraySet(String))
    maybe = Column("maybe", ArraySet(String))
    date = Column("time", DateTime)

    def __init__(self, name, date, created_by, going=[], maybe=[]):
        self.name = name
        self.created_by = created_by
        self.going = going
        self.maybe = maybe
        self.date = date

    def format(self):
        return "#{number} - **{name}** @ __{date}__. \n\t\t  Going:\t{going}\n\t\tMaybe:\t{maybe}\n".format(
            number=self.id,
            name=self.name,
            date=self.date.strftime("%I:%M%p %Z on %a, %b %d"),
            going=len(self.going),
            maybe=len(self.maybe)
        )

    def details(self):
        return "\nEVENT #{number} - **{name}** @ __{date}__ created by *{created}*\n  Going: \t{going}\nMaybe: \t{maybe}".format(
            number=self.id,
            name=self.name,
            date=self.date.strftime("%I:%M%p %Z on %a, %b %d"),
            going=", ".join(self.going) if self.going else "No one",
            maybe=", ".join(self.maybe) if self.maybe else "No one",
            created=self.created_by
        )


def connection():
    return create_engine(URL(**DATABASE))

def get_session():
    conn = connection()
    return sessionmaker(bind=conn)()

def create_database():
    db_engine = connection()
    Base.metadata.create_all(bind=db_engine)

def alter_table():
    db_engine = connection()
    db_engine.execute("DROP TABLE events")
if __name__ == "__main__":
    create_database()
    # alter_table()
