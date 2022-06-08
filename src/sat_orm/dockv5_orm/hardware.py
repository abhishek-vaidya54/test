from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates


class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=False)
    device_type_id = Column(Integer, ForeignKey("device_type.id"), nullable=False)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    firmwares = relationship("Firmware", back_populates="hardware")
    device_type = relationship("DeviceType", back_populates="hardwares")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "name": getattr(self, "name"),
            "version": getattr(self, "version"),
        }
