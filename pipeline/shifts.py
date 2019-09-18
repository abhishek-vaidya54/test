# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import ForeignKey, Column, Integer, DateTime, Text, Time, String
from sqlalchemy.orm import relationship

# Local Application Import
from database_models.pipeline.base import Base

class Shifts(Base):
    __tablename__ = 'shifts'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer,ForeignKey('warehouse.id'),nullable=False)
    name = Column(String(255), nullable=False)
    shift_start = Column(Time, nullable=False)
    shift_end = Column(Time, nullable=False)
    group_administrator = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(255), nullable=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)

    #Table Relationships
    industrial_athletes = relationship('IndustrialAthlete',backref='shifts')

    def as_dict(self):
        return {
        'id': self.id,
        'warehouse_id': self.warehouse_id,
        'name': self.name,
        'shift_start':self.shift_start,
        'shift_end':self.shift_end,
        'color':self.color,
        'description':self.description,
        'group_administrtor':self.group_administrator,
        'db_created_at':self.db_created_at,
        'db_modified_at':self.db_modified_at
    }

    def __repr__(self):
        return str(self.as_dict())

    # __table_args__ = (db.UniqueConstraint('warehouse_id', 'color'), )
    def is_match(self, time, warehouse_id = None):
        within_range = self.shift_start < time and self.shift_end > time
        if warehouse_id:
            check_warehouse = self.warehouse_id == warehouse_id
            return within_range and check_warehouse
        else:
            return within_range

