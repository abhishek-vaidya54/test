import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    DateTime,
    UnicodeText,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship

from sat_orm.pipeline_orm.pipeline_base import Base


class ResetPassword(Base):
    __tablename__ = "reset_password"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("external_admin_user.id"), nullable=False)
    ott = Column(UnicodeText, nullable=False)
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
            "ott": self.ott,
            "user_id": self.user_id,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }
