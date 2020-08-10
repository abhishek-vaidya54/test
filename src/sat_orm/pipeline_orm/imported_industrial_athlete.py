import datetime
import os
import json

from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session

from sat_orm.pipeline_orm.pipeline_base import Base

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime , desc
from sqlalchemy.orm import relationship, validates

class ImportedIndustrialAthlete(Base):
    __tablename__ = 'imported_industrial_athlete'

    id = Column(Integer, primary_key=True, autoincrement=True)

    athlete_upload_status_id = Column(Integer, ForeignKey('athlete_upload_status.id'), nullable=False)
    client = relationship(
        'AthleteUploadStatus',
        foreign_keys=athlete_upload_status_id,
        backref='athlete_upload_status'
    )
    client_id = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=False)
    schedule = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    prior_back_injuries = Column(String(255), nullable=True)

    hire_date = Column(
        DateTime,
        default=datetime.date.today(),
        nullable=True
    )

    termination_date = Column(
        DateTime,
        nullable=True
    )

    warehouse_id = Column(
        Integer,
        nullable=True
    )
    shift_id = Column(Integer, nullable=True)
    job_function_id = Column(
        Integer,
        nullable=True
    )
  
    db_created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    setting_id = Column(Integer)
    group_id = Column(Integer)

    def as_dict(self):
        return {
        "id": self.id,
        "warehouse_id": self.warehouse_id
    }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return session.query(
            ImportedIndustrialAthlete.warehouse_id
        ).filter(
            ImportedIndustrialAthlete.id == athlete_id
        ).scalar()


    def __repr__(self):
        return '%s@%s' % (self.id, self.client.id)


def get(athlete_id):
    return session.query(ImportedIndustrialAthlete).filter(
        ImportedIndustrialAthlete.id == athlete_id,
    ).scalar()
