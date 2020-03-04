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
'''

# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import ForeignKey, Column, Integer, DateTime, Text, Time, String
from sqlalchemy.orm import relationship, validates

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base

class Shifts(Base):
    __tablename__ = 'shifts'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer,ForeignKey('warehouse.id'),nullable=False)
    name = Column(String(255), nullable=False)
    shift_start = Column(Time, nullable=False)
    shift_end = Column(Time, nullable=False)
    group_administrator = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(255), nullable=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)

    #Table Relationships
    industrial_athletes = relationship('IndustrialAthlete',back_populates='shifts')
    warehouse = relationship('Warehouse',back_populates='shifts',uselist=False)

    @validates('warehouse_id')
    def validate_warehouse_id(self,key,warehouse_id):
        if warehouse_id == None:
            raise Exception('warehouse_id cannot be Null')
        else:
            return warehouse_id
    
    @validates('name')
    def validate_name(self,key,name):
        if name == None:
            raise Exception('name cannot be Null')
        else:
            return name
    
    @validates('shift_start')
    def validate_shift_start(self,key,shift_start):
        if shift_start == None:
            raise Exception('shift_start cannot be Null')
        else:
            return shift_start
    
    @validates('shift_end')
    def validate_shift_end(self,key,shift_end):
        if shift_end == None:
            raise Exception('shift_end cannot be Null')
        else:
            return shift_end
    
    @validates('group_administrator')
    def validate_group_administrator(self,key,group_administrator):
        if group_administrator == None:
            raise Exception("group_administrator cannot be Null")
        else:
            return group_administrator

    def as_dict(self):
        return {
        'id': self.id,
        'warehouse_id': self.warehouse_id,
        'name': self.name,
        'shiftStart':self.shift_start,
        'shiftEnd':self.shift_end,
        'color':self.color,
        'description':self.description,
        'group_administrtor':self.group_administrator,
        'db_created_at':self.db_created_at,
        'db_modified_at':self.db_modified_at
    }

    def __repr__(self):
        return str(self.as_dict())


