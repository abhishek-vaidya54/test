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
            view __init__.py file
'''

# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.dockv5_eventslog_orm.dockv5_eventslog_base import Base 

class RawEvemtLog(Base):
    __tablename__='raw_event_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255),nullable=True)
    dockID = Column(String(45),nullable=True)
    db_inserted_at = Column(DateTime, nullable=False,default=datetime.datetime.now())
    event_blob = Column(JSON,nullable=True)
    event_hash = Column(CHAR(32),nullable=True,unique=True)

    def as_dict(self):
        return {
            'id':self.id,
            'type':self.type,
            'dockID':self.dockID,
            'db_inserted_at':self.db_inserted_at,
            'event_blob':self.event_blob,
            'event_hash':self.event_hash
        }
    
    def __repr__(self):
        return str(self.as_dict())

