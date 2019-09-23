import datetime
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, desc
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
    def validate_client_id(self,key,client_id):
        if client_id == None:
            raise Exception('client_id cannot be Null')
        else:
            assert True
            return client_id
    
    @validates('dock_id')
    def validate_dock_id(self,key,dock_id):
        if dock_id == None:
            raise Exception('dock_id cannot be Null')
        else:
            dock_id_length = 14
            assert isinstance(dock_id,str)
            assert len(dock_id) == dock_id_length
            return dock_id
    
    @validates('warehouse_id')
    def validate_warehouse_id(self,key,warehouse_id):
        if warehouse_id == None:
            raise Exception('warehouse_id cannot be Null')
        else:
            return warehouse_id
    
    @validates('deployment_stage')
    def validate_deployment_stage(self,key,deployment_stage):
        if deployment_stage == None:
            raise Exception('deployment_stage cannot be Null')
        elif deployment_stage not in ['dev','prod']:
            raise Exception('deployment_stage can only be [dev,prod]')
        else:
            return deployment_stage

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


if __name__=="__main__":
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    connection_string = os.environ.get("CONNECTION_STRING")
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    q = session.query(Config).first()
    for dock_phase in q.dock_phases:
        print(dock_phase)