from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ReportSubscribeShiftAssociation(Base):
    __tablename__ = "report_subscribe_shift_association"

    report_subscribe_id = Column(
        Integer, ForeignKey("report_subscribe.id"), primary_key=True
    )
    shift_id = Column(Integer, ForeignKey("shifts.id"), primary_key=True)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    db_modified_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships

    report_subscribe = relationship(
        "ReportSubscribe", back_populates="report_subscribe"
    )
    shift = relationship("Shifts", back_populates="shifts")
