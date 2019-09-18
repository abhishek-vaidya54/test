# Standard Library Imports
import datetime
import json
import logging
import uuid
import re

# Third Party imports
from sqlalchemy import (ForeignKey, true, 
                        Column, Integer, String, 
                        DateTime, PrimaryKeyConstraint, 
                        UniqueConstraint, Boolean)
from sqlalchemy.orm import relationship

# Local Application Import
from database_models.pipeline.base import Base

class Client(Base):
    __tablename__ = 'client'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    db_created_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    db_modified_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow,nullable=False)
    prefix = Column(String(255), nullable=False)
    guid = Column(String(32),nullable=False)
    domain = Column(String(255),nullable=True)
    enable_processing = Column(Boolean, nullable=False, server_default=true())
    account_lock_timeout = Column(Integer,nullable=True)
    dynamic_shift = Column(Boolean,nullable=False)
    client_regex_code = Column(String(255),nullable=True)
    algo_version = Column(Integer,nullable=True)

    # Table Constraints
    PrimaryKeyConstraint('id')
    UniqueConstraint('domain','name')

    # Table Relationships
    industrial_athletes = relationship('IndustrialAthlete',backref='client')
    warehouses = relationship('Warehouse',backref='client')


    def as_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'db_created_at':self.db_created_at,
            'db_modified_at':self.db_modified_at,
            'prefix':self.prefix,
            'guid':self.guid,
            'domain':self.domain,
            'enable_processing':self.enable_processing,
            'account_lock_timeout':self.account_lock_timeout,
            'dynamic_shift':self.dynamic_shift,
            'client_regex_code':self.client_regex_code,
            'algo_version':self.algo_version
        }

    def __repr__(self):
        return str(self.as_dict())


def get_all():
    return db.session.query(Client).filter(Client.enable_processing == True).all()


def get(client_id):
    return db.session.query(Client).filter(
        Client.id == client_id,
    ).scalar()



