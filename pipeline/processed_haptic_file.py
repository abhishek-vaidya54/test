import datetime
import random
import os, sys, traceback, re

from sqlalchemy import ForeignKey, UniqueConstraint, and_, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.schema import Index
from sqlalchemy.ext.hybrid import hybrid_property

from . import commit_or_rollback, db

RUNTIME_ENV = os.environ.get("RUNTIME_ENV", "")

if RUNTIME_ENV == "LAMBDA":
    from database_models.pipeline import (
        Client,
        Fuse,
        Device,
        IndustrialAthlete,
        Warehouse,
    )
    from config import Config
else:
    from pipeline.db import Client, Fuse, Device, IndustrialAthlete, Warehouse
    from pipeline.config import Config


COMPLETE = "COMPLETE"
FAILED = "FAILED"
PROCESSING = "PROCESSING"
REPROCESS = "REPROCESS"
UNKNOWN_ATHLETE = "UNKNOWN ATHLETE"  # todo - update all values to UNKNOWN_TBD


class ProcessedHapticFile(db.Model):
    __tablename__ = "processed_haptic_file"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(255), nullable=False)

    status = db.Column(
        db.Enum(COMPLETE, PROCESSING, FAILED, UNKNOWN_ATHLETE, REPROCESS),
        nullable=False,
    )

    last_error = db.Column(db.Text)
    backtrace = db.Column(db.Text)
    last_error_time = db.Column(db.DateTime, nullable=True)
    version = db.Column(db.Integer, nullable=False)

    # todo - make this non nullable
    modified_at = db.Column(db.DateTime, nullable=True)

    bad_bends = db.Column(db.Integer, nullable=False)
    feedback_events = db.Column(db.Integer, nullable=False)

    db_created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    db_modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return self.name


def get(name, version=Config.ALGO_PROCESSING_VERSION):
    return (
        db.session.query(ProcessedHapticFile)
        .filter(
            ProcessedHapticFile.name == name,
            ProcessedHapticFile.version == version,
        )
        .one_or_none()
    )


def create(name, status, version=Config.ALGO_PROCESSING_VERSION):
    pf = ProcessedHapticFile(
        name=name,
        version=version,
        status=status,
        modified_at=datetime.datetime.utcnow(),
    )
    db.session.add(pf)
    commit_or_rollback(db.session)
    return pf


def update_status_with_message(pf, status, err_message, err_type="text"):
    now = datetime.datetime.utcnow()
    pf.last_error_time = now
    pf.last_error = err_message
    pf.backtrace = None

    if err_type == "exc":
        exc_type, exc_value, exc_traceback = sys.exc_info()
        pf.backtrace = "\n".join(
            str(trace) for trace in traceback.extract_tb(exc_traceback)
        )

    update_status(pf, status)


def update_status_with_bad_bends(pf, status, bad_bends, feedback_events):
    pf.bad_bends = bad_bends
    pf.feedback_events = feedback_events
    update_status(pf, status)


def update_status(pf, status, commit=True, err_message=None):
    now = datetime.datetime.utcnow()
    pf.status = status
    pf.modified_at = now

    if commit:
        commit_or_rollback(db.session)


def needs_processing(name, version=Config.ALGO_PROCESSING_VERSION):
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    processing_complete_or_recently_attempted = bool(
        db.session.query(ProcessedHapticFile)
        .filter(
            and_(
                ProcessedHapticFile.name == name,
                ProcessedHapticFile.version == version,
                or_(
                    ProcessedHapticFile.status.in_([COMPLETE, FAILED]),
                    and_(
                        ProcessedHapticFile.status == PROCESSING,
                        ProcessedHapticFile.modified_at > one_hour_ago,
                    ),
                ),
            )
        )
        .count()
    )
    return not processing_complete_or_recently_attempted
