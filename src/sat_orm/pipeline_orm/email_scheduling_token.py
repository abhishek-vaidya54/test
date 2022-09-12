# Standard Library Imports
import datetime, uuid

# Third Party Imports
from sqlalchemy import (
    ForeignKey,
    Column,
    UnicodeText,
    Integer,
    DateTime,
    PrimaryKeyConstraint,
)

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class EmailSchedulingToken(Base):
    __tablename__ = "email_scheduling_token"

    # Email Scheduling Token Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("report_subscribe.id"), nullable=False)
    token_id = Column(UnicodeText, nullable=False, default=uuid.uuid4)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    # Table Constraints
    PrimaryKeyConstraint("id")

    def as_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "token_id": self.token_id,
            "db_created_at": self.db_created_at,
        }
