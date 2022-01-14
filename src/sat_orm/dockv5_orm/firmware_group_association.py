from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates


class FirmwareGroupAssociation(Base):
    __tablename__ = "firmware_group_association"

    firmware_group_id = Column(
        Integer, ForeignKey("firmware_group.id"), primary_key=True
    )
    firmware_id = Column(Integer, ForeignKey("firmware.id"), primary_key=True)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships

    firmware_group = relationship(
        "FirmwareGroup", uselist=False, back_populates="firmwares"
    )
    firmware = relationship("Firmware", uselist=False, backref="firmware_groups")

    # firmware_group = relationship(
    #     "FirmwareGroup", uselist=False, back_populates="firmwares"
    # )

    # firmware = relationship("Firmware", uselist=False,
    #                         backref="firmware_groups")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "name": getattr(self, "name"),
            "description": getattr(self, "description"),
        }
