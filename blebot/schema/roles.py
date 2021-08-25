import json

from sqlalchemy import Column, String

from . import Base
from .datatypes import ArraySet

class Role(Base):
    __tablename__ = "roles"

    channel = Column("channel", String, primary_key=True)
    server = Column("server", String)
    modules = Column("modules", ArraySet(String))
    extras = Column("extras", String)

    def __init__(self, server, channel, modules, extras=None):
        self.server = server
        self.channel = channel
        self.modules = modules
        self.extras = extras or {}

    def __getattr__(self, key):
        if key == "extras":
            return json.loads(key)
        return super(Role,self).__getattr__(key)

    def __setattr__(self, key, value):
        if key == "extras":
            value = json.dumps(value)
        return super(Role, self).__setattr__(key, value)
