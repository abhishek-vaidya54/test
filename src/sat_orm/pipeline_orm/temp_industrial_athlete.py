# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, String, Integer, DateTime


# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class TempIndustrialAthlete(Base):
    __tablename__ = "temp_industrial_athlete"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(255), nullable=False)
    client_id = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=False)
    shift_id = Column(Integer, nullable=False)
    job_function_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=True)
    gender = Column(String(1), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    hire_date = Column(DateTime, default=datetime.date.today(), nullable=True)
    termination_date = Column(DateTime, nullable=True)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

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
            "db_created_at": self.db_created_at,
            "db_updated_at": self.db_updated_at,
        }

    def __repr__(self):
        return str(self.as_dict())

    def __len__(self):
        return len(self.as_dict())
