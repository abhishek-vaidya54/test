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
"""

# Standard Library Imports

# Third Party Imports
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import text
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class Rule(Base):
    __tablename__ = "rule"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    params = Column(String(1024), nullable=False)
    enabled = Column(Boolean, nullable=False, server_default="1")
    deleted = Column(Boolean, nullable=False, server_default="0")
    db_created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    db_updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )
    priority = Column(Integer, nullable=True, default=None)
    program_id = Column(Integer, nullable=True, default=None)

    @validates("name")
    def validate_name(self, key, name):
        if name is None:
            raise Exception("name cannot be Null")
        else:
            return name

    @validates("action")
    def validate_action(self, key, action):
        if action is None:
            raise Exception("action cannot be Null")
        else:
            return action

    @validates("params")
    def validate_params(self, key, params):
        if params is None:
            raise Exception("params cannot be Null")
        else:
            return params

    @validates("enabled")
    def validate_enabled(self, key, enabled):
        if enabled is None:
            raise Exception("enabled cannot be Null")
        else:
            return enabled

    @validates("deleted")
    def validate_deleted(self, key, deleted):
        if deleted is None:
            raise Exception("deleted cannot be Null")
        else:
            return deleted
