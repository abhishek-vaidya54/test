"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
            Norberto Fernandez
            Reuben Tan
            Mukul Shakya

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
"""

# Standard Library Imports
import datetime

# Third Party imports
from sqlalchemy import (
    ForeignKey,
    true,
    Column,
    Integer,
    String,
    DateTime,
    PrimaryKeyConstraint,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship, validates

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete


class Client(Base):
    __tablename__ = "client"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    prefix = Column(String(255), nullable=False)
    enable_processing = Column(Boolean, nullable=False, server_default=true())
    status = Column(String(20), nullable=False)
    contracted_users = Column(Integer, nullable=False)
    active_inactive_date = Column(DateTime, nullable=False)
    ia_name_format = Column(String(45), server_default="FIRST_NAME_LAST_NAME")

    # Table Constraints
    PrimaryKeyConstraint("id")
    UniqueConstraint("domain", "name")

    # Table Relationships
    industrial_athletes = relationship(
        "IndustrialAthlete", back_populates="client", cascade="delete, delete-orphan"
    )
    warehouses = relationship(
        "Warehouse", back_populates="client", cascade="delete, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, name):
        if name == None:
            raise Exception("name cannot be Null")
        else:
            return name

    # @validates("prefix")
    # def validate_prefix(self, key, prefix):
    #     if prefix == None:
    #         raise Exception("prefix cannot be Null")
    #     else:
    #         return prefix

    # @validates("enable_processing")
    # def validate_enable_processing(self, key, enable_processing):
    #     if enable_processing == None:
    #         raise Exception("enable_processing cannot be Null")
    #     else:
    #         return enable_processing

    # @validates("status")
    # def validate_name(self, key, status):
    #     if status == None:
    #         raise Exception("status cannot be Null")
    #     else:
    #         return status

    # @validates("contracted_users")
    # def validate_name(self, key, contracted_users):
    #     if contracted_users == None:
    #         raise Exception("contracted_users should be a valid integer")
    #     else:
    #         return contracted_users

    # @validates("active_inactive_date")
    # def validate_name(self, key, active_inactive_date):
    #     if active_inactive_date == None:
    #         raise Exception("active_inactive_date cannot be Null")
    #     else:
    #         return active_inactive_date

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
            "prefix": self.prefix,
            "enable_processing": self.enable_processing,
        }

    def __repr__(self):
        return str(self.as_dict())


def insert(session, data):
    """
        Description
            checks to see if client_id is in table,
            if it is, then only update the none primary key items.
            else return 0.

        params
            session: sqlalchemy.orm.session.Session
            data: {key: value} dictionary

        return
            Returns client id and commits to database
    """
    client_id = data["id"]
    client_in_table = session.query(Client).filter_by(id=client_id).first()
    if client_in_table:
        return 0
    else:
        client = Client(
            name=data["name"], enable_processing=data["enableProcessing"], prefix=""
        )
        session.add(client)
        session.commit()
        session.refresh(client)
        return client.id


def update(session, data):
    """
        Description
            checks to see if client_id is in table,
            if it is, then only update the none primary key items.
            else return 0.

        params
            session: sqlalchemy.orm.session.Session
            data: {key: value} dictionary

        return
            Returns client id and commits to database
    """
    client_id = data["client_id"]
    client_in_table = session.query(Client).filter_by(id=client_id).first()
    if client_in_table:
        data["enable_processing"] = data["enableProcessing"]
        data.pop("client_id", None)
        data.pop("enableProcessing", None)
        session.query(Client).filter_by(id=client_id).update(data)
        session.commit()
        return client_id
    else:
        return 0


def delete(session, data):
    """
        Description
            Deletes a client by the id.

        params
            session: sqlalchemy.orm.session.Session
            data: {key: value} dictionary
    """
    response = {}
    client_id = data["client_id"]

    client_has_warehouse = has_warehouse(session, client_id)
    if client_has_warehouse:
        response["error"] = "Client has warehouse"
        response[
            "message"
        ] = "Ensure that client has no athlete/warehouse before deleting"
        return response

    client_has_athlete = has_athlete(session, client_id)
    if client_has_athlete:
        response["error"] = "Client has athlete"
        response[
            "message"
        ] = "Ensure that client has no athlete/warehouse before deleting"
        return response

    no_of_deleted_rows = session.query(Client).filter_by(id=client_id).delete()
    # session.delete(client)
    if no_of_deleted_rows == 1:
        session.commit()
    else:
        response["error"] = "Error deleting client"

    return response


def has_warehouse(session, client_id):
    """
        Description
            Checks if there is any warehouse associated with the client.

        params
            session: sqlalchemy.orm.session.Session
            client_id: Integer

        returns
            True: When there is a warehouse which belongs to the client
            False: When there is no warehouse which belongs to the client
    """
    client_has_warehouse = (
        session.query(Warehouse).filter_by(client_id=client_id).first()
    )
    if client_has_warehouse:
        return True
    else:
        return False


def has_athlete(session, client_id):
    """
        Description
            Checks if there is any athlete associated with the client.

        params
            session: sqlalchemy.orm.session.Session
            client_id: Integer

        returns
            True: When there is a athlete which belongs to the client
            False: When there is no athlete which belongs to the client
    """
    client_has_athlete = (
        session.query(IndustrialAthlete).filter_by(client_id=client_id).first()
    )
    if client_has_athlete:
        return True
    else:
        return False
