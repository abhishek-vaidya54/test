# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.dockv5_eventslog_orm.dockv5_eventslog_base import Base 

class SensorEvents(Base):
    __tablename__='sensor_events'

    id = Column(Integer,primary_key=True,autoincrement=True)
    timestamp = Column(DateTime,nullable=False)
    type = Column(String(45),nullable=True)
    dockID = Column(String(45),nullable=True)
    clientID = Column(String(45),nullable=True)
    warehouseID = Column(String(45), nullable=True)
    assignment_time = Column(Integer,nullable=True)
    sensorID = Column(String(45),nullable=True)
    athleteID = Column(String(45), nullable=True)
    datarecord_count = Column(Integer,nullable=True)
    port = Column(Integer,nullable=True)
    db_inserted_at = Column(DateTime,default=datetime.datetime.now(),nullable=False)
    firmware_version = Column(String(45),nullable=True)
    sessionID = Column(String(45), nullable=True)
    datapage_count = Column(Integer,nullable=True)

    @validates('timestamp')
    def validate_timestamp(self,key,timestamp):
        if timestamp == None:
            raise Exception('timestamp cannot be Null')
        else:
            return timestamp
    
    def as_dict(self):
        return {
            'id':self.id,
            'timestamp':self.timestamp,
            'type':self.type,
            'dockID':self.dockID,
            'clientID':self.clientID,
            'warehouseID':self.warehouseID,
            'assignment_time':self.assignment_time,
            'sensorID':self.sensorID,
            'athleteID':self.athleteID,
            'datarecord_count':self.datarecord_count,
            'port':self.port,
            'db_inserted_at':self.db_inserted_at,
            'firmware_version':self.firmware_version,
            'sessionID':self.sessionID,
            'datapage_count':self.datapage_count
        }
    
    def __repr__(self):
        return str(self.as_dict())

