from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, validates


class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(255), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    firmwares = relationship("Firmware", back_populates="hardware")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "version": getattr(self, "version")
        }
