# Standard Library Import
import datetime

# Third Party Import
from sqlalchemy import ForeignKey,PrimaryKeyConstraint, UniqueConstraint, Column, String, Integer, DateTime, Float, Boolean 
from sqlalchemy.orm import relationship

# Local Application Import 
from database_models.pipeline.base import Base

class Warehouse(Base):
    __tablename__ = 'warehouse'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    prefered_timezone = Column(String(100),server_default='UTC',nullable=False)
    algo_version = Column(Integer, nullable=True)
    display_names = Column(Boolean, nullable=False)
    utc_op_day_start = Column(String(45), nullable=False)
    week_start = Column(String(45), nullable=False)
    show_engagement = Column(Boolean,nullable=False)
    update_engagement = Column(Boolean, nullable=False)
    hide_judgement = Column(Boolean,nullable=False)
    standard_score = Column(Float,nullable=True)
    min_safety_score = Column(Float,nullable=True)
    max_safety_score = Column(Float,nullable=True)
    first_quarter_safety_score = Column(Float,nullable=True)
    median_safety_score = Column(Float,nullable=True)
    third_quarter_safety_score = Column(Float,nullable=True)

    # Table Constraints
    PrimaryKeyConstraint('id')

    # Table relationships
    industrial_athletes = relationship("IndustrialAthlete", backref='warehouse')
    job_functions = relationship('JobFunction',backref='warehouse')
    shifts = relationship('Shifts',backref='warehouse')
    

    def as_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'name': self.name,
            'location': self.location,
            'db_created_at':self.db_created_at,
            'db_modified_at':self.db_modified_at,
            'prefered_timezone': self.prefered_timezone,
            'algo_version':self.algo_version,
            'display_names':self.display_names,
            'utc_op_day_start':self.utc_op_day_start,
            'week_start':self.week_start,
            'show_engagment':self.show_engagement,
            'update_engagement':self.update_engagement,
            'hide_judgement':self.hide_judgement,
            'standard_score':self.standard_score,
            'min_safety_score':self.min_safety_score,
            'max_safety_score':self.max_safety_score,
            'first_quarter_safety_score':self.first_quarter_safety_score,
            'median_safety_score':self.median_safety_score,
            'third_quarter_safety_score':self.third_quarter_safety_score
        }

    def __repr__(self):
        return str(self.as_dict())


# class Masquerade(db.Model):
#     __tablename__ = 'masquerade'
#     __table_args__ = (db.UniqueConstraint('original_warehouse_id', ),)

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     enable = db.Column(db.Boolean, nullable=False, default=False)
#     original_warehouse_id = db.Column(
#         db.Integer,
#         ForeignKey('warehouse.id'),
#         nullable=True
#     )
#     original_warehouse = db.relationship(
#         'Warehouse',
#         foreign_keys=original_warehouse_id,
#         backref='masqurades'
#     )

#     masquerade_warehouse_id = db.Column(
#         db.Integer,
#         ForeignKey('warehouse.id'),
#         nullable=True
#     )
#     masquerade_warehouse = db.relationship(
#         'Warehouse',
#         foreign_keys=masquerade_warehouse_id,
#         backref='masquerade'
#     )

#     db_created_at = db.Column(
#         db.DateTime,
#         default=datetime.datetime.utcnow,
#         nullable=False
#     )
#     db_modified_at = db.Column(
#         db.DateTime,
#         default=datetime.datetime.utcnow,
#         onupdate=datetime.datetime.utcnow,
#         nullable=False
#     )

