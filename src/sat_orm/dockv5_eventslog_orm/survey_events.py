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


class SurveyEvents(Base):
    __tablename__ = "survey_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    type = Column(String(45), nullable=True)
    athleteID = Column(String(45), nullable=True)
    content_id = Column(String(45), nullable=True)
    response = Column(String(45), nullable=True)
    db_inserted_at = Column(DateTime, default=datetime.datetime.now(), nullable=True)
    firmware_version = Column(String(45), nullable=True)
    clientID = Column(String(50), nullable=True)
    warehouseID = Column(String(50), nullable=True)

    @validates("timestamp")
    def validate_timestamp(self, key, timestamp):
        if timestamp == None:
            raise Exception("timestamp cannot be Null")
        else:
            return timestamp

    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "athleteID": self.athleteID,
            "content_id": self.content_id,
            "response": self.response,
            "db_inserted_at": self.db_inserted_at,
            "firmware_version": self.firmware_version,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID,
        }

    def __repr__(self):
        return str(self.as_dict())
