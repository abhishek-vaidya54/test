# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import Column, Integer, String, DateTime, CHAR, JSON
from sqlalchemy.orm import validates

# Local Application Imports
from dockv5_eventslog_orm.dockv5_eventslog_base import Base 
class EngagementStats(Base):
    __tablename__ = 'engagement_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    athlete_id = Column(Integer(11), unique=True, nullable=False)
    total_days_worn = Column(Integer(11), nullable=True, default='0')
    total_hours_worn = Column(Integer(11), nullable=True, default='0')
    last_checkin = Column(DateTime, nullable=True, default=None)
    last_checkout = Column(DateTime, nullable=True, default=None)
    db_created_at = Column(DateTime, nullable=True, default=None)
    db_modified_at = Column(DateTime, nullable=True, default=None)
    days_worn_haptic_enable = Column(Integer,nullable=False,default='0')
    days_worn_haptic_disable = Column(Integer,nullable=False,default='0')

    def as_dict(self):
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "total_days_worn": self.total_days_worn,
            "total_hours_worn": self.total_hours_worn,
            "last_checkin": self.last_checkin,
            "last_checkout": self.last_checkout,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
            "days_worn_haptic_enable":self.days_worn_haptic_enable,
            "days_worn_haptic_disable":self.days_worn_haptic_disable
        }

    def __repr__(self):
        return str(self.as_dict())

        