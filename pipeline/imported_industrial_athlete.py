import datetime
import os
import json

from sqlalchemy import ForeignKey, and_, or_, event
from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session
from . import commit_or_rollback, db


class ImportedIndustrialAthlete(db.Model):
    __tablename__ = 'imported_industrial_athlete'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    athlete_upload_status_id = db.Column(db.Integer, ForeignKey('athlete_upload_status.id'), nullable=False)
		client = db.relationship(
        'AthleteUploadStatus',
        foreign_keys=athlete_upload_status_id,
        backref='athlete_upload_status'
    )
    client_id = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    prior_back_injuries = db.Column(db.String(255), nullable=True)

    hire_date = db.Column(
        db.DateTime,
        default=datetime.date.today(),
        nullable=True
    )

    termination_date = db.Column(
        db.DateTime,
        nullable=True
    )

    warehouse_id = db.Column(
        db.Integer,
        nullable=True
    )
    shift_id = db.Column(db.Integer, nullable=True)
    job_function_id = db.Column(
        db.Integer,
        nullable=True
    )
  
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

    setting_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)

    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id
    }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return db.session.query(
            ImportedIndustrialAthlete.warehouse_id
        ).filter(
            ImportedIndustrialAthlete.id == athlete_id
        ).scalar()


    def __repr__(self):
        return '%s@%s' % (self.id, self.client.id)


def get(athlete_id):
    return db.session.query(ImportedIndustrialAthlete).filter(
        ImportedIndustrialAthlete.id == athlete_id,
    ).scalar()
