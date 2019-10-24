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

# Third Party Library Imports
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import text
from sqlalchemy.orm import validates

# Local Application Imports 
from sat_orm.pipeline_orm.pipeline_base import Base

class Setting(Base):
    __tablename__='settings'

    # Columns
    id = Column(Integer,primary_key=True,autoincrement=True)
    target_type = Column(String(45),nullable=False)
    target_id = Column(Integer,nullable=False)
    value = Column(JSON,nullable=True,server_default=None)
    db_created_at = Column(DateTime,nullable=True, server_default=text('CURRENT_TIMESTAMP'))

    # Relationship

    @validates('target_type')
    def validate_target_type(self,key,target_type):
        if target_type is None:
            raise Exception('target_type cannot be Null')
        else:
            return target_type
    
    @validates('target_id')
    def validate_target_id(self,key,target_id):
        if target_id is None:
            raise Exception('target_id cannot be Null')
        else:
            return target_id
    
    def as_dict(self):
        return {
            'id':self.id,
            'target_type':self.target_type,
            'target_id':self.target_id,
            'value':self.value,
            'db_created_at':self.db_created_at
        }
    
    def __repr__(self):
        return str(self.as_dict())
    
    