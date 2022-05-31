from sat_orm.pipeline_orm.pipeline_base import Base
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ReportSubscribeWarehouseAssociation(Base):
    __tablename__ = "report_subscribe_warehouse_association"

    report_subscribe_id = Column(
        Integer, ForeignKey("report_subscribe.id"), primary_key=True
    )
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), primary_key=True)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    db_modified_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships

    report_subscribe = relationship("ReportSubscribe", back_populates="warehouse")
