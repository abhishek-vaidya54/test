"""
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
"""

# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.dockv5_eventslog_orm.dockv5_eventslog_base import Base


class AppcrashLog(Base):
    __tablename__ = "appcrash_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    log = Column(String(5000), nullable=False)
    dockID = Column(String(12), nullable=False)

    @validates("timestamp")
    def validate_timestamp(self, key, timestamp):
        if timestamp == None:
            raise Exception("timestamp cannot be Null")
        else:
            return timestamp

    @validates("log")
    def validate_log(self, key, log):
        if log == None:
            raise Exception("log cannot be Null")
        else:
            return log

    @validates("dockID")
    def validate_dockID(self, key, dockID):
        if dockID == None:
            raise Exception("dockID cannot be Null")
        else:
            return dockID

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "log": self.log,
            "dockID": self.dockID,
        }

    def __repr__(self):
        return str(self.as_dict())
