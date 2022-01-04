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
        default="JPEG",
    )
    url = Column(String(255), nullable=False)
    created_by = Column(
        Integer, ForeignKey("external_admin_user.id"), primary_key=True
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
            "user_id": self.user_id,
            "title": self.title,
            "short_description": self.short_description,
            "icon_type": self.icon_type,
            "hyperlink_address": self.hyperlink_address,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return str(self.as_dict())