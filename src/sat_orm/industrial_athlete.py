# Standard Library Imports
import datetime
import os
import json

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, validates


# Local Application Imports
from sat_orm.pipeline_base import Base

class IndustrialAthlete(Base):
    __tablename__ = 'industrial_athlete'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    gender = Column(String(1), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=False)
    schedule = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    prior_back_injuries = Column(String(255), nullable=True)
    hire_date = Column(DateTime, default=datetime.date.today(),nullable=True)
    termination_date = Column(DateTime,nullable=True)
    warehouse_id = Column(Integer,ForeignKey('warehouse.id'),nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    job_function_id = Column(Integer,ForeignKey('job_function.id'),nullable=False)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    setting_id = Column(Integer,nullable=True)
    group_id = Column(Integer,nullable=True)

    # Table Relationships
    client = relationship('Client', back_populates='industrial_athletes',uselist=False)
    warehouse = relationship('Warehouse',back_populates='industrial_athletes',uselist=False)
    shifts = relationship('Shifts',back_populates='industrial_athletes',uselist=False)
    job_function = relationship('JobFunction',back_populates='industrial_athletes',uselist=False)

    @validates('client_id')
    def validate_client_id(self,key,client_id):
        if client_id == None:
            raise Exception('client_id cannot be Null')
        else:
            return client_id

    @validates('gender')
    def validate_gender(self,key,gender):
        if gender == None:
            raise Exception('gender cannot be Null')
        else:
            return gender
    
    @validates('first_name')
    def validate_first_name(self,key,first_name):
        if first_name == None:
            raise Exception('first_name cannot be Null')
        else:
            return first_name
    
    @validates('last_name')
    def validate_last_name(self,key,last_name):
        if last_name == None:
            raise Exception('last_name cannot be Null')
        else:
            return last_name

    
    @validates('external_id')
    def validate_external_id(self,key,external_id):
        if external_id == None:
            raise Exception('external_id cannot be Null')
        else:
            return external_id
    
    @validates('warehouse_id')
    def validate_warehouse_id(self,key,warehouse_id):
        if warehouse_id == None:
            raise Exception('warehouse_id cannot be Null')
        else:
            return warehouse_id
    
    @validates('shift_id')
    def validate_shift_id(self,key,shift_id):
        if shift_id == None:
            raise Exception('shift_id cannot be Null')
        else:
            return shift_id
    
    @validates('job_function_id')
    def validate_job_function_id(self,key,job_function_id):
        if job_function_id == None:
            raise Exception('job_function_id cannot be Null')
        else:
            return job_function_id
    
    def as_dict(self):
        return {
        'id': self.id,
        'client_id':self.client_id,
        'warehouse_id': self.warehouse_id,
        'job_function_id':self.job_function_id,
        'shift_id':self.shift_id,
        'first_name':self.first_name,
        'last_name':self.last_name,
        'gender':self.gender,
        'external_id':self.external_id,
        'db_created_at':self.db_created_at,
        'db_modified_at':self.db_modified_at
    }

    def __repr__(self):
        return str(self.as_dict())
    
    def __len__(self):
        return len(self.as_dict())
    
