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

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from sqlalchemy.sql import text

# Local Imports
from sat_orm.pipeline_orm.pipeline_base import Base 

class BinaryBucketMonitor(Base):
    __tablename__='binary_bucket_monitor'

    # Columns
    id = Column(Integer,primary_key=True,autoincrement=True)
    sensor_id = Column(String(50),nullable=True)
    athlete_id = Column(String(50),nullable=True)
    dock_id = Column(String(50),nullable=True)
    client_id = Column(String(50),nullable=True)
    warehouse_id = Column(String(50),nullable=True)
    firmware_version = Column(String(50),nullable=True)
    assignment_time = Column(String(45),nullable=True)
    session_id = Column(String(50),nullable=True)
    db_created = Column(DateTime,server_default=text('CURRENT_TIMESTAMP'),nullable=True)
    db_modified = Column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),nullable=False)
    file_size = Column(String(50),nullable=True)

    # relationships

    @validates('session_id')
    def validate_session_id(self,key,sensor_id):
        if sensor_id is None:
            raise Exception('session_id cannot be Null')
        else:
            return sensor_id
    
    @validates('db_modified')
    def validate_db_mofied(self,key,db_modified):
        if db_modified is None:
            raise Exception('db_modified cannot be Null')
        else:
            return db_modified
    

