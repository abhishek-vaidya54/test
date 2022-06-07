from sat_orm.pipeline_orm.pipeline_base import Base
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ReportSubscribeJobFunctionAssociation(Base):
    __tablename__ = "report_subscribe_job_function_association"

    report_subscribe_id = Column(
        Integer, ForeignKey("report_subscribe.id"), primary_key=True
    )
    job_function_id = Column(Integer, ForeignKey("job_function.id"), primary_key=True)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    db_modified_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    report_subscribe = relationship("ReportSubscribe", back_populates="job_functions")

    job_function = relationship("JobFunction", backref="report_subscribe")
