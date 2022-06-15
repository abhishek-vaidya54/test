# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    DateTime,
    PrimaryKeyConstraint,
    VARCHAR,
)

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class EmailLogs(Base):
    __tablename__ = "email_logs"

    # Notification Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_email = Column(String(150), nullable=False)
    destination_email = Column(VARCHAR(255), nullable=False)
    report_subscribed = Column(VARCHAR(255), nullable=False)
    status = Column(VARCHAR(255), nullable=False)
    error_message = Column(VARCHAR(255), nullable=False)
    created_by = Column(Integer, ForeignKey("external_admin_user.id"), nullable=False)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    # Table Constraints
    PrimaryKeyConstraint("id")

    def as_dict(self):
        return {
            "id": self.id,
            "source_email": self.created_by,
            "destination_email": self.title,
            "report_subscribed": self.description,
            "status": self.type,
            "error_message": self.url,
            "created_by": self.is_active,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }
