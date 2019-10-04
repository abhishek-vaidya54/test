# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates

# Local Application Imports
from sat_orm.dockv5_orm.dockv5_base import Base


class DockPhase(Base):
    __tablename__="dock_phase"
    
    # Table inputs
    id = Column(Integer,primary_key=True,autoincrement=True)
    dock_id = Column(String,ForeignKey('config.dock_id'),nullable=False)
    timestamp = Column(DateTime,default=datetime.datetime.now(),nullable=False)
    phase = Column(Enum('PREP','DEMO','INFIELD','MAINTENANCE','UNUSED','RETIRED'),nullable=False)
    deployment_stage = Column(String(20), nullable=False)

    @validates('dock_id')
    def validate_dock_id(self,key,dock_id):
        if dock_id == None:
            raise Exception('dock_id cannot be Null')
        else:
            return dock_id
    
    @validates('timestamp')
    def validate_timestamp(self,key,timestamp):
        if timestamp == None:
            raise Exception('timestamp cannot be Null')
        else:
            return timestamp
    
    @validates('phase')
    def validate_phase(self,key,phase):
        if phase == None:
            raise Exception('phase cannot be Null')
        else:
            return phase
    
    @validates('deployment_stage')
    def validate_deployment_stage(self,key,deployment_stage):
        if deployment_stage == None:
            raise Exception('deployment_stage cannot be Null')
        else:
            return deployment_stage

    def as_dict(self):
        return {
            'id':self.id,
            'dock_id':self.dock_id,
            'timestamp':self.timestamp,
            'phase':self.phase,
            'deployment_stage':self.deployment_stage
        }
    
    def __repr__(self):
        return str(self.as_dict())
