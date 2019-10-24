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
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import validates
from sqlalchemy.sql import text

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base

class ParserMonitor(Base):
    __tablename__='parser_monitor'

    # Columns
    ID = Column(Integer,primary_key=True, autoincrement=True)
    sensor_id = Column(String(50),default=None,nullable=True)
    athlete_id = Column(String(50),default=None,nullable=True)
    dock_id = Column(String(50),default=None,nullable=True)
    client_id = Column(String(50),default=None,nullable=True)
    warehouse_id = Column(String(50),default=None,nullable=True)
    firmware_version = Column(String(50),default=None,nullable=True)
    assignment_time = Column(String(45),default=None,nullable=True)
    session_id = Column(String(50),nullable=False)
    db_created = Column(DateTime,server_default=text('CURRENT_TIMESTAMP'),nullable=True)
    db_modified = Column(DateTime,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),nullable=False)
    file_status = Column(String(50),default='parsing',nullable=False)
    message = Column(String(50),default=None,nullable=True)
    file_size = Column(String(50),default=None,nullable=True)

    # Relationships

    @validates('session_id')
    def validate_session_id(self,key,session_id):
        if session_id is None:
            raise Exception('session_id cannot be Null')
        else:
            return session_id
    
    @validates('db_modified')
    def validate_db_modified(self,key,db_modified):
        if db_modified is None:
            raise Exception('db_modified cannot be Null')
        else:
            return db_modified
    
    @validates('file_status')
    def validate_file_status(self,key,file_status):
        if file_status is None:
            raise Exception('file_status cannot be Null')
        else:
            return file_status
    
