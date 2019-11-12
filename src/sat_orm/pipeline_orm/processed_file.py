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

# Third Library Imports
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base

class ProcessedFile(Base):
    __tablename__='processed_file'

    # Columns
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),nullable=False)
    status = Column(Enum('COMPLETE','PROCESSING','FAILED','TOO SMALL','UNKNOWN ATHLETE','REPROCESS'),nullable=False)
    version = Column(Integer,nullable=False)
    db_created_at = Column(DateTime,nullable=False)
    db_modified_at = Column(DateTime,nullable=False)
    last_error = Column(Text,nullable=True)
    backtrace = Column(Text,nullable=True)
    last_error_time = Column(DateTime,nullable=True)
    lateral_angle_exceeded_limit = Column(Integer,nullable=False)
    lateral_vel_exceeded_limit = Column(Integer,nullable=False)
    twist_vel_exceeded_limit = Column(Integer,nullable=False)
    cropping_time = Column(Integer,nullable=False)
    cropping_percentage = Column(Float,nullable=False)
    work_time = Column(Integer,nullable=False)
    sg_position_limit = Column(Integer,nullable=False)
    start_time = Column(DateTime,nullable=True)
    end_time = Column(DateTime,nullable=True)
    athlete_id = Column(Integer,nullable=True)
    client_id = Column(Integer,nullable=True)
    warehouse_id = Column(Integer,nullable=True)
    job_function_id = Column(Integer,nullable=True)
    sensor_id = Column(String(45),nullable=True)
    group_id = Column(Integer,nullable=True)
    setting_id = Column(Integer,nullable=True)
    session_id = Column(String(45),nullable=True)

    # Relationship

    @validates('name')
    def validate_name(self,key,name):
        if name is None:
            raise Exception('name cannot be Null')
        else:
            return name
    
    @validates('status')
    def validate_status(self,key,status):
        if status is None:
            raise Exception('status cannot be Null')
        else:
            return status
    
    @validates('version')
    def validate_version(self,key,version):
        if version is None:
            raise Exception('version cannot be Null')
        else:
            return version
    
    @validates('db_created_at')
    def validate_db_created_at(self,key,db_created_at):
        if db_created_at is None:
            raise Exception('db_created_at cannot be Null')
        else:
            return db_created_at
    
    @validates('db_modified_at')
    def validate_db_modified_at(self,key,db_modified_at):
        if db_modified_at is None:
            raise Exception('db_modified_at cannot be Null')
        else:
            return db_modified_at
    
    @validates('lateral_angle_exceeded_limit')
    def validate_lateral_angle_exceeded_limit(self,key,lateral_angle_exceeded_limit):
        if lateral_angle_exceeded_limit is None:
            raise Exception('lateral_angle_exceeded_limit cannot be Null')
        else:
            return lateral_angle_exceeded_limit
    
    @validates('lateral_vel_exceeded_limit')
    def validate_lateral_vel_exceeded_limit(self,key,lateral_vel_exceeded_limit):
        if lateral_vel_exceeded_limit is None:
            raise Exception('lateral_vel_exceeded_limit cannot be Null')
        else:
            return lateral_vel_exceeded_limit
    
    @validates('twist_vel_exceeded_limit')
    def validate_twist_vel_exceeded_limit(self, key, twist_vel_exceeded_limit):
        if twist_vel_exceeded_limit is None:
            raise Exception('twist_vel_exceeded_limit cannot be Null')
        else:
            return twist_vel_exceeded_limit
    

    @validates('cropping_time')
    def validate_cropping_time(self,key,cropping_time):
        if cropping_time is None:
            raise Exception('cropping_time cannot be Null')
        else:
            return cropping_time
    
    @validates('cropping_percentage')
    def validate_cropping_percentage(self,key,cropping_percentage):
        if cropping_percentage is None:
            raise Exception('cropping_percentage cannot be Null')
        else:
            return cropping_percentage
    
    @validates('work_time')
    def validate_work_time(self,key,work_time):
        if work_time is None:
            raise Exception('work_time cannot be Null')
        else:
            return work_time
    
    @validates('sg_position_limit')
    def validate_sg_position_limit(self,key,sg_position_limit):
        if sg_position_limit is None:
            raise Exception('sg_position_limit cannot be Null')
        else:
            return sg_position_limit
    


    