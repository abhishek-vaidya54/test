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


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    enable_processing = db.Column(db.Boolean, nullable=False, server_default=true())
    db_created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    db_modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    def as_dict(self):
        return {
            "prefix": getattr(self, "prefix"),
            "name": getattr(self, "name"),
        }

    def __repr__(self):
        return self.name


def get_all():
    return db.session.query(Client).filter(Client.enable_processing == True).all()


def get(client_id):
    return (
        db.session.query(Client)
        .filter(
            Client.id == client_id,
        )
        .scalar()
    )
