import datetime
import os
import json

from sqlalchemy import ForeignKey, and_, or_, event
from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session
from . import commit_or_rollback, db


class IndustrialAthlete(db.Model):
    __tablename__ = 'industrial_athlete'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    client_id = db.Column(db.Integer, ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client',
        foreign_keys=client_id,
        backref='athletes'
    )
    gender = db.Column(db.String(1), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    prior_back_injuries = db.Column(db.String(255), nullable=True)

    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('athletes')
    )

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
        ForeignKey('warehouse.id'),
        nullable=True
    )
    warehouse = db.relationship(
        'Warehouse',
        foreign_keys=warehouse_id,
        backref='athletes'
    )
    shift_id = db.Column(db.Integer, ForeignKey('shifts.id'), nullable=True)
    shift = db.relationship(
        'Shifts',
        foreign_keys=shift_id,
        backref='athletes'
    )
    job_function_id = db.Column(
        db.Integer,
        ForeignKey('job_function.id'),
        nullable=True
    )
    job_function = db.relationship(
        'JobFunction',
        foreign_keys=job_function_id,
        backref='athletes'
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

    settings = db.Column(db.Text)
    # setting_id = db.Column(db.Integer)
    # group_id = db.Column(db.Integer)

    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id
    }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return db.session.query(
            IndustrialAthlete.warehouse_id
        ).filter(
            IndustrialAthlete.id == athlete_id
        ).scalar()


    def __repr__(self):
        return '%s@%s' % (self.id, self.client.id)


def get(athlete_id):
    return db.session.query(IndustrialAthlete).filter(
        IndustrialAthlete.id == athlete_id,
    ).scalar()