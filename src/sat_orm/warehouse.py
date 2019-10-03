# Standard Library Import
import datetime

# Third Party Import
from sqlalchemy import ForeignKey,PrimaryKeyConstraint, UniqueConstraint, Column, String, Integer, DateTime, Float, Boolean 
from sqlalchemy.orm import relationship, validates

# Local Application Import 
from sat_orm.pipeline_base import Base

class Warehouse(Base):
    __tablename__ = 'warehouse'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    prefered_timezone = Column(String(100),server_default='UTC',nullable=False)
    algo_version = Column(Integer, nullable=True)
    display_names = Column(Boolean, nullable=False)
    utc_op_day_start = Column(String(45), nullable=False)
    week_start = Column(String(45), nullable=False)
    show_engagement = Column(Boolean,nullable=False)
    update_engagement = Column(Boolean, nullable=False)
    hide_judgement = Column(Boolean,nullable=False)
    # standard_score = Column(Float,nullable=True)
    # min_safety_score = Column(Float,nullable=True)
    # max_safety_score = Column(Float,nullable=True)
    # first_quarter_safety_score = Column(Float,nullable=True)
    # median_safety_score = Column(Float,nullable=True)
    # third_quarter_safety_score = Column(Float,nullable=True)

    # Table Constraints
    PrimaryKeyConstraint('id')

    # Table relationships
    client = relationship('Client',back_populates='warehouses',uselist=False)
    industrial_athletes = relationship("IndustrialAthlete", back_populates='warehouse')
    job_functions = relationship('JobFunction',back_populates='warehouse')
    shifts = relationship('Shifts',back_populates='warehouse')
    
    @validates('client_id')
    def validate_client_id(self,key,client_id):
        if client_id == None:
            raise Exception('client_id cannot be Null')
        else:
            return client_id
    
    @validates('name')
    def validate_name(self,key,name):
        if name == None:
            raise Exception('name cannot be Null')
        else:
            return name
    
    @validates('prefered_timezone')
    def validate_prefered_timezone(self,key,prefered_timezone):
        if prefered_timezone == None:
            raise Exception('prefered_timezone cannot be Null')
        else:
            return prefered_timezone
    
    @validates('display_names')
    def validate_display_names(self,key,display_names):
        if display_names == None:
            raise Exception('display_names cannot be Null')
        else:
            return display_names
    
    @validates('show_engagement')
    def validate_show_engagement(self,key,show_engagement):
        if show_engagement == None:
            raise Exception('show_engagement cannot be Null')
        else:
            return show_engagement
    
    @validates('update_engagement')
    def validate_update_engagement(self,key,update_engagement):
        if update_engagement == None:
            raise Exception("update_engagement cannot be Null")
        else:
            return update_engagement
    
    @validates('hide_judgement')
    def validate_hide_judgement(self,key,hide_judgement):
        if hide_judgement == None:
            raise Exception('hide_judgement cannot be Null')
        else:
            return hide_judgement

    def as_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'name': self.name,
            'location': self.location,
            'db_created_at':self.db_created_at,
            'db_modified_at':self.db_modified_at,
            'prefered_timezone': self.prefered_timezone,
            'algo_version':self.algo_version,
            'display_names':self.display_names,
            'utc_op_day_start':self.utc_op_day_start,
            'week_start':self.week_start,
            'show_engagment':self.show_engagement,
            'update_engagement':self.update_engagement,
            'hide_judgement':self.hide_judgement,
        }

    def __repr__(self):
        return str(self.as_dict())


# 'standard_score':self.standard_score,
#             'min_safety_score':self.min_safety_score,
#             'max_safety_score':self.max_safety_score,
#             'first_quarter_safety_score':self.first_quarter_safety_score,
#             'median_safety_score':self.median_safety_score,
#             'third_quarter_safety_score':self.third_quarter_safety_score