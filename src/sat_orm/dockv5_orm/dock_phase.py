'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************

DESCRIPTION:
            The dockv5_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.
            
            +---------------+
            | Dockv5 Tables |
            +---------------+
            | config        |
            | dock_phase    |
            +---------------+

            **** Edit This File If tables are added or removed ****
'''

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
    phase = Column(Enum('DEPLOYED','NOT DEPLOYED','MAINTENANCE'),nullable=False,default='NOT DEPLOYED')
    deployment_stage = Column(String(20), nullable=False)

    config = relationship('Config',back_populates='dock_phase')
    configs = relationship('Config',back_populates='dock_phases')

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
    
    def update_phase(self,session,Config,DockPhase,data):
        ''' checks to see if the phase changed, if it did,
            a new row will be added to dock_phase. If there is no dock_id,
            add the new dock_id
        '''
        current_config = session.query(Config).filter_by(dock_id=data.get('dock_id',None)).first()
        if (current_config.dock_phase == None or data.get('phase',None) != current_config.dock_phase.phase):
            dock_phase = DockPhase(dock_id=data.get('dock_id',None),phase=data.get('phase',None),deployment_stage=data.get('deployment_stage',None))
            session.add(dock_phase)

            


