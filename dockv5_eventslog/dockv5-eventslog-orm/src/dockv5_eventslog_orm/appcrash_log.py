# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from dockv5_eventslog_orm.dockv5_eventslog_base import Base 

class AppcrashLog(Base):
    __tablename__ = 'appcrash_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    log = Column(String(5000), nullable=False)
    dockID = Column(String(12), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "log": self.log,
            "dockID": self.dockID
        }

    def __repr__(self):
        return str(self.as_dict())