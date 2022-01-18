import datetime
import os
import json

from sqlalchemy import ForeignKey, and_, or_, event
from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session
from . import commit_or_rollback, db


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    target_id = db.Column(db.Integer)
    target_type = db.Column(db.Text)

    value = db.Column(db.JSON)

    db_created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    def as_dict(self):
        return {"id": self.id, "value": self.value}

    def __repr__(self):
        return "%s@%s" % (self.id, self.value)


def get(setting_id):
    return (
        db.session.query(Settings)
        .filter(
            Settings.id == setting_id,
        )
        .scalar()
    )
