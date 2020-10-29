import datetime
import os
import json

from sqlalchemy.orm import backref
from sqlalchemy.orm import object_session

from sat_orm.pipeline_orm.pipeline_base import Base

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, desc, Enum
from sqlalchemy.orm import relationship, validates


class ImportedIndustrialAthlete(Base):
    __tablename__ = "imported_industrial_athlete"

    id = Column(Integer, primary_key=True, autoincrement=True)

    athlete_upload_status_id = Column(
        Integer,
        ForeignKey("athlete_upload_status.id", ondelete="CASCADE"),
        nullable=False,
    )
    athlete_upload_status = relationship(
        "AthleteUploadStatus",
        foreign_keys=athlete_upload_status_id,
        backref="athlete_upload_status",
    )

    gender = Column(String(1), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=False)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    hire_date = Column(DateTime, default=datetime.date.today(), nullable=False)
    termination_date = Column(DateTime, nullable=True)

    client_id = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=True)
    shift_id = Column(Integer, nullable=True)
    job_function_id = Column(Integer, nullable=True)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    group_id = Column(Integer, nullable=True)

    on_duplicate_action = Column(
        Enum("deactivate_and_insert", "update"),
        nullable=True,
    )
    ia_id = Column(Integer, nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "warehouse_id": self.warehouse_id,
            "job_function_id": self.job_function_id,
            "shift_id": self.shift_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "external_id": self.external_id,
            "weight": self.weight,
            "height": self.height,
            "hire_date": self.hire_date,
            "termination_date": self.termination_date,
        }

    @classmethod
    def get_warehouse_id(self, athlete_id):
        return (
            session.query(ImportedIndustrialAthlete.warehouse_id)
            .filter(ImportedIndustrialAthlete.id == athlete_id)
            .scalar()
        )

    # def __repr__(self):
    #     return "%s@%s" % (self.id, self.client.id)
