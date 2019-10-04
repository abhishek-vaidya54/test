# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON, Float
from sqlalchemy.orm import validates

# Local Application Imports
from sat_orm.dockv5_eventslog_orm.dockv5_eventslog_base import Base 

class MonthlySafety(Base):
    __tablename__ = 'monthly_safety'

    id = Column(Integer, primary_key=True, autoincrement=True)
    athlete_id = Column(Integer(), nullable=False)
    latest_safety_score = Column(Float, default=0.0)
    monthly_score = Column(Float, nullable=False, default=0.0)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime, default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)


    def as_dict(self):
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "latest_safety_score":self.latest_safety_score,
            "monthly_score": self.monthly_score,
            "db_created_at":self.db_created_at,
            "db_modified_at":self.db_modified_at
        }

    def __repr__(self):
        return str(self.as_dict())

