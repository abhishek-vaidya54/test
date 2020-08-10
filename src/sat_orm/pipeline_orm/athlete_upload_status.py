import datetime
import json
import logging
import uuid
import re

from sqlalchemy import ForeignKey, true, false
from sqlalchemy.dialects.mysql import INTEGER

from itsdangerous import TimedJSONWebSignatureSerializer
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime , desc
from sqlalchemy.orm import relationship, validates

logger = logging.getLogger(__name__)
from sat_orm.pipeline_orm.pipeline_base import Base

class AthleteUploadStatus(Base):
    __tablename__ = 'athlete_upload_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    processed = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    db_created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    db_updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )


    def as_dict(self):
        return {
            'processed': getattr(self, 'processed'),
            'total': getattr(self, 'total'),
        }

    def __repr__(self):
        return self.id

