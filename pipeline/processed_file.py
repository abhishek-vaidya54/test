import datetime
import random
import sys, traceback
import os
import re

from sqlalchemy import ForeignKey, UniqueConstraint, and_, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.schema import Index
from sqlalchemy.ext.hybrid import hybrid_property

from . import commit_or_rollback, db

DEPLOYMENT_STAGE = os.environ.get("DEPLOYMENT_STAGE", "")

from config_DEV import Config as ConfigDev
from config_PROD import Config as ConfigProd

Config = None

if DEPLOYMENT_STAGE == "PROD":
    Config = ConfigProd
else:
    Config = ConfigDev


from database_models.pipeline import Client, IndustrialAthlete, Warehouse


COMPLETE = "COMPLETE"
FAILED = "FAILED"
NOT_ENOUGH_DATA = "TOO SMALL"
PROCESSING = "PROCESSING"
REPROCESS = "REPROCESS"
UNKNOWN_ATHLETE = "UNKNOWN ATHLETE"  # todo - update all values to UNKNOWN_TBD


class ProcessedFile(db.Model):
    __tablename__ = "processed_file"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(255), nullable=False)
    status = db.Column(
        db.Enum(
            COMPLETE, PROCESSING, FAILED, NOT_ENOUGH_DATA, UNKNOWN_ATHLETE, REPROCESS
        ),
        nullable=False,
    )

    last_error = db.Column(db.Text)
    backtrace = db.Column(db.Text)
    last_error_time = db.Column(db.DateTime, nullable=True)
    version = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    # todo - make this non nullable
    sg_position_limit = db.Column(db.Integer, default=0)
    lateral_angle_exceeded_limit = db.Column(db.Integer, default=0)
    lateral_vel_exceeded_limit = db.Column(db.Integer, default=0)
    twist_vel_exceeded_limit = db.Column(db.Integer, default=0)

    cropping_time = db.Column(db.Integer, default=0)
    work_time = db.Column(db.Integer, default=0)
    cropping_percentage = db.Column(db.Integer, default=0)

    db_created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    db_modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    cropping_time = db.Column(db.Integer, default=0)

    athlete_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    sensor_id = db.Column(db.Text)
    setting_id = db.Column(db.Integer)
    job_function_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    session_id = db.Column(db.Text)
    stl_write_status = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("name", "version"),)

    @hybrid_property
    def num_minutes(self):
        return self.work_time / 60.0

    def __repr__(self):
        return self.name


def get(name, version=Config.ALGO_PROCESSING_VERSION):
    return (
        db.session.query(ProcessedFile)
        .filter(ProcessedFile.name == name, ProcessedFile.version == version)
        .scalar()
    )


def create(
    name,
    athlete_data=None,
    settings_data=None,
    file_params=None,
    status=PROCESSING,
    version=Config.ALGO_PROCESSING_VERSION,
):
    pf = None

    if athlete_data is not None:
        group_id = (
            settings_data.target_id
            if settings_data and settings_data.target_type == "group"
            else athlete_data.group_id
        )
        pf = ProcessedFile(
            name=name,
            version=version,
            athlete_id=athlete_data.id,
            client_id=athlete_data.client_id,
            warehouse_id=athlete_data.warehouse_id,
            job_function_id=athlete_data.job_function.id,
            sensor_id=file_params["sensor_id"],
            group_id=group_id,
            setting_id=int(file_params["setting_id"]),
            session_id=file_params["session_id"],
            status=status,
        )
    else:
        pf = ProcessedFile(
            name=name,
            version=version,
            athlete_id=0,
            client_id=0,
            warehouse_id=0,
            job_function_id=0,
            sensor_id=file_params["sensor_id"],
            group_id=0,
            setting_id=int(file_params["setting_id"]),
            session_id=file_params["session_id"],
            status=status,
        )

    db.session.add(pf)
    commit_or_rollback(db.session)
    return pf


def update_start_end_time(pf, start, end):
    start_time = datetime.datetime.utcfromtimestamp(int(start))
    end_time = datetime.datetime.utcfromtimestamp(int(end))
    print(start_time, end_time)
    pf.start_time = start_time
    pf.end_time = end_time
    commit_or_rollback(db.session)


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


def update_status_with_smart_limits(
    pf, status, smart_limits=None, cropped_time=0, total_time=0
):
    if smart_limits:
        pf.sg_position_limit = int(smart_limits.sg_position_limit)
        pf.lateral_angle_exceeded_limit = int(smart_limits.lateral_angle_exceeded_limit)
        pf.lateral_vel_exceeded_limit = int(smart_limits.lateral_vel_exceeded_limit)
        pf.twist_vel_exceeded_limit = int(smart_limits.twist_vel_exceeded_limit)

    pf.cropping_time = int(cropped_time / 1000)
    pf.work_time = int((total_time - cropped_time) / 1000)
    pf.cropping_percentage = round((float(cropped_time) / float(total_time)) * 100, 1)

    update_status(pf, status)


def update_status(pf, status, commit=True, err_message=None):
    now = datetime.datetime.utcnow()
    pf.status = status
    pf.db_modified_at = now

    if commit:
        commit_or_rollback(db.session)


def needs_processing(name, version=Config.ALGO_PROCESSING_VERSION):
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    processing_complete_or_recently_attempted = bool(
        db.session.query(ProcessedFile)
        .filter(
            and_(
                ProcessedFile.name == name,
                ProcessedFile.version == version,
                or_(
                    ProcessedFile.status.in_([COMPLETE, FAILED, NOT_ENOUGH_DATA]),
                    and_(
                        ProcessedFile.status == PROCESSING,
                        ProcessedFile.db_modified_at > one_hour_ago,
                    ),
                ),
            )
        )
        .count()
    )
    return not processing_complete_or_recently_attempted


def update_stl_write_status(pf, status, commit=True, err_message=None):
    now = datetime.datetime.utcnow()
    pf.stl_write_status = status
    pf.db_modified_at = now

    if commit:
        commit_or_rollback(db.session)
