import datetime
import json
import logging
import uuid
import re

from sqlalchemy import ForeignKey, true, false
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy.dialects.mysql import INTEGER

from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app
from . import db

logger = logging.getLogger(__name__)


class AthleteUploadStatus(db.Model):
    __tablename__ = 'athlete_upload_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    processed = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    db_created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    db_modified_at = db.Column(
        db.DateTime,
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

