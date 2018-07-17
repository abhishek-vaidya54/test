import datetime
import os

from sqlalchemy.orm import object_session
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import synonym_for
from sqlalchemy.schema import Index

from . import commit_or_rollback, db

from utilities import util


class Risk(db.Model):
    __tablename__ = 'risk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    processed_file_id = db.Column(
        db.Integer,
        sa.ForeignKey('processed_file.id'),
        nullable=True
    )
    processed_file = db.relationship(
        'ProcessedFile',
        foreign_keys=[processed_file_id],
        backref='risks'
    )

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    avg_twist_velocity = db.Column(db.Integer)
    lift_rate = db.Column(db.Integer)
    max_flexion = db.Column(db.Integer)
    average_flexion = db.Column(db.Integer)
    max_lateral = db.Column(db.Integer)
    average_lateral = db.Column(db.Integer)
    max_lateral_velocity = db.Column(db.Float)
    max_moment = db.Column(db.Float)
    risk_score = db.Column(db.Float)

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

    __table_args__ = (
        Index('risk_start_end_index', 'start_time', 'end_time'),
    )

    @hybrid_property
    def safety_score(self):
        return 100 - self.risk_score

    def __repr__(self):
        return 'Risk from %s for %s' % (
            self.processed_file.name, self.processed_file.athlete.name)


def create(rows, processed_file_id, commit=True):
    assert all((isinstance(row, util.OutputRow) for row in rows))

    for row in rows:
        risk = Risk(
            processed_file_id=processed_file_id,
            start_time=row.window_start,
            end_time=row.window_end,
            lift_rate=row.lift_rate,
            max_lateral_velocity=row.max_lateral_velocity,
            max_flexion=row.max_flexion,
            average_flexion=row.average_flexion,
            max_lateral=row.max_lateral,
            average_lateral=row.average_lateral,
            avg_twist_velocity=row.avg_twist_velocity,
            risk_score=row.risk_score,
            max_moment=row.max_moment
            )
        db.session.add(risk)

    if commit:
        commit_or_rollback(db.session)