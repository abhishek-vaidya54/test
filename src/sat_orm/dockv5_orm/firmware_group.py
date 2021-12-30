import datetime
from sat_orm.dockv5_orm.dockv5_base import Base
from sat_orm.dockv5_orm.firmware_group_association import FirmwareGroupAssociation
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, validates


class FirmwareGroup(Base):
    __tablename__ = "firmware_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    firmwares = relationship(FirmwareGroupAssociation,
                             back_populates=__tablename__)

    configs = relationship("Config", back_populates="firmware_group")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "name": getattr(self, "name"),
            "description": getattr(self, "description")
        }
