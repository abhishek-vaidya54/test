# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, Float, Text,Boolean,PrimaryKeyConstraint
from sqlalchemy.orm import relationship

# Local Application Imports
from database_models.pipeline.base import Base

class JobFunction(Base):
    __tablename__ = 'job_function'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer,ForeignKey('warehouse.id'),nullable=False)
    name = Column(String(255), nullable=False)
    max_package_mass = Column(Float, default=6.6)
    group_administrator = Column(String(255), nullable=False)
    max_package_weight = Column(Integer, nullable=True)
    min_package_weight = Column(Integer, nullable=True)
    avg_package_weight = Column(Integer, nullable=True)
    lbd_indicence = Column(Boolean, nullable=True, default=False)
    lbd_indicence_rate = Column(Integer, nullable=True )
    description = Column(Text, nullable=True)
    color = Column(String(255), nullable=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    standard_score = Column(Float)
    min_safety_score = Column(Float,nullable=True)
    max_safety_score = Column(Float,nullable=True)
    first_quarter_safety_score = Column(Float,nullable=True)
    median_safety_score = Column(Float,nullable=True)
    third_quarter_safety_score = Column(Float,nullable=True)

    # Table Constraints
    PrimaryKeyConstraint('id')
    
    # Table Relationships
    industrial_athletes = relationship('IndustrialAthlete',backref='jub_function')
    
    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id,
        "name": self.name,
        'max_package+mass':self.max_package_mass,
        'group_administrator':self.group_administrator,
        'max_package_weight':self.max_package_weight,
        'min_package_weight':self.min_package_weight,
        'avg_package_weight':self.avg_package_weight,
        'lbd_indicence': self.lbd_indicence,
        'lbd_indicence_rate':self.lbd_indicence_rate,
        'description':self.description,
        'color':self.color,
        'db_created_at':self.db_created_at,
        'db_modified_at':self.db_modified_at,
        'standard_score':self.standard_score,
        'min_safety_score':self.min_safety_score,
        'max_safety_score':self.max_safety_score,
        'first_quarter_safety_score':self.first_quarter_safety_score,
        'median_safety_score':self.median_safety_score,
        'third_quarter_safety_score':self.third_quarter_safety_score
        }

    def __repr__(self):
        return str(self.as_dict())


def get(job_function_id):
    return db.session.query(JobFunction).filter(
        JobFunction.id == job_function_id,
    ).one_or_none()
