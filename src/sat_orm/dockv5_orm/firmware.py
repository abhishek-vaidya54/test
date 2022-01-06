from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from sat_orm.dockv5_orm.firmware_group_association import FirmwareGroupAssociation


class Firmware(Base):
    __tablename__ = "firmware"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(255), nullable=False)
    s3_url = Column(String(255), nullable=True)
    device_type_id = Column(Integer, ForeignKey(
        "device_type.id"), nullable=False)
    hardware_id = Column(Integer, ForeignKey("hardware.id"), nullable=False)

    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    hardware = relationship(
        "Hardware", back_populates="firmwares")
    device_type = relationship(
        "DeviceType", back_populates="firmwares")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "version": getattr(self, "version"),
            "s3_url": getattr(self, "s3_url")
        }
