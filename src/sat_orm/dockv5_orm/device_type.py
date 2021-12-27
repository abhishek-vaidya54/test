from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, validates


class DeviceType(Base):
    __tablename__ = "device_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    firmwares = relationship("Firmwares", back_populates="device_type")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "name": getattr(self, "name")
        }
