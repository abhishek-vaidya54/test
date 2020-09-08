import datetime
import logging
from sqlalchemy import Column, String, Integer, DateTime

logger = logging.getLogger(__name__)
from sat_orm.pipeline_orm.pipeline_base import Base


class BulkUploadLog(Base):
    __tablename__ = "bulk_upload_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    count = Column(Integer, nullable=True)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
