'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
'''

# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime , desc
from sqlalchemy.orm import relationship, validates


# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base


class IndustrialAthlete(Base):
    __tablename__ = 'industrial_athlete'

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    gender = Column(String(1), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=False)
    schedule = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    prior_back_injuries = Column(String(255), nullable=True)
    hire_date = Column(DateTime, default=datetime.date.today(), nullable=True)
    termination_date = Column(DateTime, nullable=True)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    job_function_id = Column(Integer, ForeignKey(
        'job_function.id'), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(DateTime, default=datetime.datetime.utcnow,
                            onupdate=datetime.datetime.utcnow, nullable=False)
    setting_id = Column(Integer, nullable=True)
    group_id = Column(Integer, nullable=True)
    job_function_change_date = Column(DateTime, nullable=True)
    gender_change_date = Column(DateTime, nullable=True)

    # Table Relationships
    client = relationship(
        'Client', back_populates='industrial_athletes', uselist=False)
    warehouse = relationship(
        'Warehouse', back_populates='industrial_athletes', uselist=False)
    shifts = relationship(
        'Shifts', back_populates='industrial_athletes', uselist=False)
    job_function = relationship(
        'JobFunction', back_populates='industrial_athletes', uselist=False)

    @validates('client_id')
    def validate_client_id(self, key, client_id):
        if client_id == None:
            raise Exception('client_id cannot be Null')
        else:
            return client_id

    @validates('gender')
    def validate_gender(self, key, gender):
        if gender == None:
            raise Exception('gender cannot be Null')
        else:
            return gender

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if first_name == None:
            raise Exception('first_name cannot be Null')
        else:
            return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if last_name == None:
            raise Exception('last_name cannot be Null')
        else:
            return last_name

    @validates('external_id')
    def validate_external_id(self, key, external_id):
        if external_id == None:
            raise Exception('external_id cannot be Null')
        else:
            return external_id

    @validates('warehouse_id')
    def validate_warehouse_id(self, key, warehouse_id):
        if warehouse_id == None:
            raise Exception('warehouse_id cannot be Null')
        else:
            return warehouse_id

    @validates('shift_id')
    def validate_shift_id(self, key, shift_id):
        if shift_id == None:
            raise Exception('shift_id cannot be Null')
        else:
            return shift_id

    @validates('job_function_id')
    def validate_job_function_id(self, key, job_function_id):
        if job_function_id == None:
            raise Exception('job_function_id cannot be Null')
        else:
            return job_function_id

    def as_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'warehouse_id': self.warehouse_id,
            'job_function_id': self.job_function_id,
            'shift_id': self.shift_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'external_id': self.external_id,
            'db_created_at': self.db_created_at,
            'db_modified_at': self.db_modified_at
        }

    def __repr__(self):
        return str(self.as_dict())

    def __len__(self):
        return len(self.as_dict())



def get_all_athletes(session):
    """
        Generic select * from industrial_athlete where column = value for value in filter_args
    """
    return session.query(IndustrialAthlete).all()



def dockv5_getAthletes_select_by_client_warehouse_not_terminated(session,client_id, warehouse_id):
    """
        Implements the below query in the DockV5-API getAthletes lambda:
        SELECT * FROM industrial_athlete WHERE client_id= %s AND warehouse_id= %s AND termination_date is NULL;', (client_id, warehouse_id)
    """
    return session.query(IndustrialAthlete) \
        .filter(IndustrialAthlete.client_id == client_id, IndustrialAthlete.warehouse_id == warehouse_id, IndustrialAthlete.termination_date.isnot(None)).all()


def dockv5_getEngagement_select_by_id(session,id):
    """
        Implements the below query in the DockV5-API getEngagement lambda:
        'SELECT * FROM industrial_athlete WHERE id=%s LIMIT 1',(athlete_id)
    """
    return session.query(IndustrialAthlete).filter(IndustrialAthlete.id == id).first()


def dockv5_getUpdatedAthletes_select_group_id(session,client_id, warehouse_id):
    """
        Implements the below query in the DockV5-API getUpdatedAthletes lambda:
        select group_id from industrial_athlete where client_id = %s and warehouse_id = %s)
    """
    return session.query(IndustrialAthlete.group_id) \
        .filter(IndustrialAthlete.client_id == client_id, IndustrialAthlete.warehouse_id == warehouse_id).all()


def dockv5_getUpdatedAthletes_select_id(session,client_id, warehouse_id):
    """
        Implements the below query in DockV5-API getUpdatedAthletes lambda:
        select id from industrial_athlete where client_id = %s and warehouse_id = %s
    """
    return session.query(IndustrialAthlete.id) \
        .filter(IndustrialAthlete.client_id == client_id, IndustrialAthlete.warehouse_id == warehouse_id).all()


def dockv5_getUpdatedAthletes_select_by_db_modified(session,last_checked_timestamp):
    """
        Implements the below query in DockV5-API getUpdatedAthletes lambda:
        select * from industrial_athlete where db_modified_at > %s order by db_modified_at DESC;
    """
    return session.query(IndustrialAthlete) \
        .filter(IndustrialAthlete.db_modified_at > last_checked_timestamp) \
        .order_by(IndustrialAthlete.db_modified_at).all()

# TODO ''


def dockv5_getUpdatedAthletes_select_by_client_warehouse_db_modified(session,client_id, warehouse_id, last_athlete_check):


    """
        Implements the below query in DockV5-API getUpdatedAthletes lambda:
        'select * from industrial_athlete where client_id = %s and warehouse_id = %s and db_modified_at > %s order by db_modified_at DESC'
    """
    return session.query(IndustrialAthlete) \
        .filter(IndustrialAthlete.client_id == client_id, IndustrialAthlete.warehouse_id == warehouse_id, IndustrialAthlete.db_modified_at > last_athlete_check) \
        .order_by(desc(IndustrialAthlete.db_modified_at))

    """
    TODO
    /Users/matthewmacneille/dev/DockV5-API/endpoints/getUpdatedAthletes/lambda_handler.py:
    select * from industrial_athlete where client_id = %s and warehouse_id = %s and id in (select target_id from settings where target_type = %s and db_created_at > %s);

    /Users/matthewmacneille/dev/DockV5-API/endpoints/rulesEngine/lambda_handler.py:
    SELECT * FROM industrial_athlete WHERE id=%s LIMIT 1
    SELECT job_function_id FROM industrial_athlete WHERE id = %s
    SELECT warehouse_id FROM industrial_athlete WHERE id = %s

    /Users/matthewmacneille/dev/DockV5-API/endpoints/templateEndpoint/lambda_handler.py:
    'SELECT first_name, last_name, id, external_id, settings FROM industrial_athlete WHERE client_id=%s AND warehouse_id=%s ORDER BY first_name ASC
    """
