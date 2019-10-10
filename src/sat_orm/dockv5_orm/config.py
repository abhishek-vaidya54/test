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
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, desc

# Local Application Imports
from sat_orm.dockv5_orm.dockv5_base import Base

class Config(Base):
    __tablename__ = 'config'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    dock_id = Column(String(45),nullable=True, unique=True)
    dock_imei = Column(String(45),nullable=True)
    client_id = Column(Integer,nullable=True)
    warehouse_id = Column(Integer,nullable=True)
    deployment_stage = Column(String(45),default="DEV",nullable=True)
    barcode_regex = Column(String(45),nullable=True)
    firware_version = Column(Integer,nullable=True)
    description = Column(String(500),nullable=True)

    # Relationships 
    dock_phase = relationship('DockPhase',order_by='DockPhase.timestamp.desc()',back_populates='config',uselist=False)
    dock_phases = relationship('DockPhase',order_by='DockPhase.timestamp.desc()',back_populates='configs')

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
            "barcode_regex":self.barcode_regex,
            "firmware_version":self.firmware_version,
            "description":self.description
        }

    def __repr__(self):
        return str(self.as_dict())


