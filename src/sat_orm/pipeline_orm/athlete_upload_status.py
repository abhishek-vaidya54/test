from sat_orm.pipeline_orm.pipeline_base import Base
import datetime
import json
import logging
import uuid
import re

from sqlalchemy import ForeignKey, true, false
from sqlalchemy.dialects.mysql import INTEGER

from itsdangerous import TimedJSONWebSignatureSerializer
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, desc
from sqlalchemy.orm import relationship, validates

logger = logging.getLogger(__name__)


class AthleteUploadStatus(Base):
    __tablename__ = "athlete_upload_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    processed = Column(Integer, nullable=False)
    batch = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    connection_id = Column(String(30), nullable=True)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "username": getattr(self, "username"),
            "processed": getattr(self, "processed"),
            "batch": getattr(self, "batch"),
            "total": getattr(self, "total"),
            "client_id": getattr(self, "client_id"),
            "connection_id": getattr(self, "connection_id"),
        }

    # def __repr__(self):
    #     return "%s" % (self.id)
