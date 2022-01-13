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


class KeepaliveEvents(Base):
    __tablename__ = "keepalive_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    type = Column(String(45), nullable=True, default=None)
    dockID = Column(String(45), nullable=True, default=None)
    db_inserted_at = Column(DateTime, nullable=True, default=None)
    batt_percent = Column(String(45), nullable=True, default=None)
    charge_status = Column(String(45), nullable=True, default=None)
    clientID = Column(String(50), nullable=True, default=None)
    warehouseID = Column(String(50), nullable=True, default=None)
    dockIMEI = Column(String(45), nullable=True, default=None)
    enum_ports = Column(String(100), nullable=True, default=None)
    occupied_ports = Column(String(100), nullable=True, default=None)
    local_sensor_fw = Column(Integer, nullable=True, default=None)
    app_version = Column(String(45), nullable=True, default=None)

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
            "dockID": self.dockID,
            "db_inserted_at": self.db_inserted_at,
            "batt_percent": self.batt_percent,
            "charge_status": self.charge_status,
            "clientID": self.clientID,
            "warehouseID": self.warehouseID,
            "dockIMEI": self.dockIMEI,
            "enum_porta": self.enum_ports,
            "occupied_ports": self.occupied_ports,
            "local_sensor_fw": self.local_sensor_fw,
            "app_version": self.app_version,
        }

    def __repr__(self):
        return "keepalive event for dock %s" % (self.dockID)
