import datetime
from sqlalchemy import Column, Integer, String, DateTime

from . import  Base
from .datatypes import ArraySet

class Roles(Base):
    __tablename__ = "roles"

    id = Column("id", Integer, primary_key=True)
    server = Column("server", String)
    channel = Column("channel", String)
    module = Column("module", String)
    metadata = Column("metadata", String)

    def __init__(self, server, message, module, metadata=None):
        self.server = server
        self.message = message
        self.module = module
        self.metadata = metadata or {}
