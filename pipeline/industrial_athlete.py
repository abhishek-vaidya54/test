# Standard Library Imports
import datetime
import os
import json

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import backref, relationship


# Local Application Imports
from database_models.pipeline.base import Base

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
    warehouse_id = Column(Integer,ForeignKey('warehouse.id'),nullable=True)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)
    job_function_id = Column(Integer,ForeignKey('job_function.id'),nullable=True)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    setting_id = Column(Integer)
    group_id = Column(Integer)

    # Table Relationships
    # warehouse = db.relationship('Warehouse',foreign_keys=warehouse_id,backref='industrial_athlete')
    # shift = db.relationship('Shifts',foreign_keys=shift_id, backref='industrial_athlete')
    # job_function = db.relationship('JobFunction',foreign_keys=job_function_id,backref='industrial_athlete')
    # client = db.relationship('Client',foreign_keys=client_id,backref='industrial_athlete')
    

    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id
    }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return db.session.query(
            IndustrialAthlete.warehouse_id
        ).filter(
            IndustrialAthlete.id == athlete_id
        ).scalar()


    def __repr__(self):
        return str(self.as_dict())
    
    def __len__(self):
        return len(self.as_dict())
    


def get(athlete_id):
    return db.session.query(IndustrialAthlete).filter(
        IndustrialAthlete.id == athlete_id,
    ).scalar()
