# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    PrimaryKeyConstraint,
    Enum,
    VARCHAR
)

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base

class Notification(Base):
    __tablename__ = "notification"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    type = Column(
        Enum("update", "news", "warning", "event"),
        nullable=False,
        default="news",
    )
    url = Column(String(255), nullable=False)
    created_by = Column(
        Integer, ForeignKey("external_admin_user.id"), nullable=False
    )
    is_active = Column(Boolean, nullable=True, default=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
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
            "created_by": self.created_by,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "url": self.url,
            "is_active": self.is_active,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    