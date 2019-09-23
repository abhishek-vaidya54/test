from sqlalchemy.orm import relationship, validates
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum, desc
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Config(Base):
    __tablename__ = 'config'

    # Table Inputs
    id = Column(Integer, primary_key=True, autoincrement=True)
    dock_id = Column(String(45))
    client_id = Column(Integer)
    warehouse_id = Column(Integer)
    deployment_stage = Column(String(45))

    # Relationships 
    dock_phases = relationship('DockPhase',order_by='DockPhase.timestamp.desc()')

    @validates('client_id')
    def validate_client_id(self, key, client_id):
        assert client_id != None
        assert isinstance(client_id,int)
        return client_id
    
    @validates('dock_id')
    def validate_dock_id(self,key,dock_id):
        dock_id_length = 14
        assert dock_id != None
        assert isinstance(dock_id,str)
        assert len(dock_id) == dock_id_length
        return dock_id

    def as_dict(self):
        return {
            "id": self.id,
            "dock_id": self.dock_id,
            "client_id": self.client_id,
            "warehouse_id": self.warehouse_id,
            "deployment_stage": self.deployment_stage,
            "dock_phases":self.dock_phases
        }

    def __repr__(self):
        return str(self.as_dict())

class DockPhase(Base):
    __tablename__="dock_phase"
    id = Column(Integer,primary_key=True,autoincrement=True)
    dock_id = Column(String,nullable=False)
    timestamp = Column(DateTime,nullable=False)
    phase = Column(Enum('PREP','DEMO','INFIELD','MAINTENANCE','UNUSED','RETIRED'),nullable=False)

    def as_dict(self):
        return {
            'id':self.id,
            'config_id':self.config_id,
            'timestamp':self.timestamp,
            'phase':self.phase,
        }
    
    def __repr__(self):
        return str(self.as_dict())
