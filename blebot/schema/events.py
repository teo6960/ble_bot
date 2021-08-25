from sqlalchemy import Column, Integer, String, DateTime
import humanize

from . import  Base
from .datatypes import ArraySet

class Event(Base):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    created_by = Column("created_by", String)
    going = Column("going", ArraySet(String))
    maybe = Column("maybe", ArraySet(String))
    date = Column("time", DateTime)
    server = Column("column", String)
    channel = Column("channel", String)

    def __init__(self, name, date, created_by, channel_id, server_id, going=[], maybe=[]):
        self.name = name
        self.created_by = created_by
        self.going = going
        self.maybe = maybe
        self.date = date
        self.server = server_id
        self.channel = channel_id

    def format(self):
        return "#{number} - **{name}** @ __{date}__. \n\t\t  Going:\t{going}\n\t\tMaybe:\t{maybe}\n".format(
            number=self.id,
            name=self.name,
            # date=self.date.strftime("%I:%M%p %Z on %a, %b %d"),
            date=humanize.naturaldate(self.date),
            going=len(self.going),
            maybe=len(self.maybe)
        )

    def details(self):
        return "\nEVENT #{number} - **{name}** @ __{date}__ created by *{created}*\n  Going: \t{going}\nMaybe: \t{maybe}".format(
            number=self.id,
            name=self.name,
            # date=self.date.strftime("%I:%M%p %Z on %a, %b %d"),
            date=humanize.naturaldate(self.date),
            going=", ".join(self.going) if self.going else "No one",
            maybe=", ".join(self.maybe) if self.maybe else "No one",
            created=self.created_by
        )
