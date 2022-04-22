import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    DateTime,
    Unicode,
    UnicodeText,
    PrimaryKeyConstraint,
    Enum,
)
from sqlalchemy.orm import relationship

from sat_orm.pipeline_orm.pipeline_base import Base


class ReportSubscribe(Base):
    __tablename__ = "report_subscribe"
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_emails = Column(UnicodeText, nullable=False)
    report_name = Column(Unicode(255), nullable=False)
    subscription_type = Column(
        Enum("Daily", "Weekly", "Monthly"),
        nullable=False,
        default="Daily",
    )
    subscribed_by = Column(
        Integer, ForeignKey("external_admin_user.id"), nullable=False
    )
    db_created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )
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
            "to_emails": self.to_emails,
            "report_name": self.report_name,
            "subscription_type": self.subscription_type,
            "subscribed_by": self.subscribed_by,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }
