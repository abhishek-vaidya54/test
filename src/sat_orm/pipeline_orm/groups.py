from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

# Local Application Imports 
from sat_orm.pipeline_orm.pipeline_base import Base

class Groups(Base):
    __tablename__ = "groups"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    description = Column(String(45), nullable=True)
    db_created_at = Column(DateTime, nullable=True, server_default=text('CURRENT_TIMESTAMP'))
    override_settings = Column(TINYINT(1), nullable=False)

    # Table Relationships
    industrial_athletes = relationship('IndustrialAthlete',back_populates='groups')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'db_created_at': self.db_created_at,
            'override_settings': self.override_settings
        }

    def __repr__(self):
        return str(self.as_dict())
