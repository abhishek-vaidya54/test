# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from dockv5_eventslog_orm.dockv5_eventslog_base import Base 

class DataEvents(Base):
    __tablename__ = 'data_events'

    id = Column(Integer, primary_key=True, autoincrement=True)

    timestamp = Column(DateTime, nullable=True, default=None)
    type = Column(String(45), nullable=True, default=None)
    sensorID = Column(String(45), nullable=True, default=None)
    firmware_version = Column(String(45), nullable=True, default=None)
    datarecord_count = Column(Integer(20), nullable=True, default=None)
    db_inserted_at = Column(DateTime, nullable=True, default=None)
    assignment_time = Column(Integer(20), nullable=True, default=None)
    filename = Column(String(100), nullable=True, default=None)
    dockID = Column(String(45), nullable=True, default=None)
    warehouseID = Column(String(45), nullable=True, default=None)
    athleteID = Column(String(45), nullable=True, default=None)
    clientID = Column(String(45), nullable=True, default=None)
    port = Column(Integer(10), nullable=True, default=None)
    sessionID = Column(String(45), nullable=True, default=None)

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.event_type,
            "sensorID": self.sensorID,
            "firmware_version": self.firmware_version,
            "datarecord_count": self.datarecord_count,
            "db_inserted_at": self.db_inserted_at,
            "assignment_time": self.assignment_time,
            "filename": self.filename,
            "dockID": self.dockID,
            "warehouseID": self.warehouseID,
            "athleteID": self.athleteID,
            "clientID": self.clientID,
            "port": self.port,
            "sessionID": self.sessionID
        }

    def __repr__(self):
        return str(self.as_dict())