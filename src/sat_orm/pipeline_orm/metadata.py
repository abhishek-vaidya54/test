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
from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import validates
from sqlalchemy.sql import text

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class Metadata(Base):
    __tablename__ = "metadata"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(45), nullable=False)
    processed_file_id = Column(Integer, nullable=False)
    metadata_type = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    exclude = Column(Boolean, nullable=False)
    db_created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    notes = Column(JSON, nullable=True)

    # Relationships

    @validates("session_id")
    def validate_session_id(self, key, session_id):
        if session_id is None:
            raise Exception("session_id cannot be Null")
        else:
            return session_id

    @validates("processed_file_id")
    def validate_processed_file_id(self, key, processed_file_id):
        if processed_file_id is None:
            raise Exception("processed_file_id cannot be Null")
        else:
            return processed_file_id

    @validates("metadata_type")
    def validate_metadata_type(self, key, metadata_type):
        if metadata_type is None:
            raise Exception("metadata_type cannot be Null")
        else:
            return metadata_type

    @validates("value")
    def validate_value(self, key, value):
        if value is None:
            raise Exception("value cannot be Null")
        else:
            return value

    @validates("exclude")
    def validate_exclude(self, key, exclude):
        if exclude is None:
            raise Exception("exclude cannot be Null")
        else:
            return exclude

    @validates("db_created_at")
    def validate_db_created_at(self, key, db_created_at):
        if db_created_at is None:
            raise Exception("db_created_at cannot be Null")
        else:
            return db_created_at
