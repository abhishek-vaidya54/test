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
    event,
)
from sqlalchemy.orm import relationship, validates

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete
from sat_orm.pipeline_orm.utilities import client_utils
from sat_orm.pipeline_orm.utilities import utils
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


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
    subdomain = Column(String(255), nullable=True)

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
            "status": self.status,
            "contracted_users": self.contracted_users,
            "active_inactive_date": self.active_inactive_date,
            "ia_name_format": self.ia_name_format,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(Client, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Helper method to check if params are valid for updating a single client
    Input:
        param_input: json containing data to be updated for a single client.
                        id field MUST be inside.
    Output:
        Return [True, None] if all params are valid.
        Returns [False, Errors] if there are params which are not valid
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value

    errors = []

    if "name" in params_input:
        is_valid, message = client_utils.is_valid_client_name(
            connection, params_input.get("name", ""), params_input.get("id", "")
        )
        if not is_valid:
            errors.append(build_error("name", message))

    if "status" in params_input:
        is_valid = client_utils.is_valid_client_status(params_input.get("status", ""))
        if not is_valid:
            errors.append(build_error("status", constants.INVALID_CLIENT_STATUS_MESSAGE))

    if "contracted_users" in params_input:
        is_valid, message = utils.is_valid_int(
            params_input.get("contracted_users", "")
        )
        if not is_valid:
            errors.append(build_error("contracted_users", message))

    if "active_inactive_date" in params_input:
        is_valid, date_obj = utils.is_valid_date(
            params_input.get("active_inactive_date", "")
        )
        if not is_valid:
            errors.append(build_error("active_inactive_date", constants.INVALID_DATE_MESSAGE))

    if "ia_name_format" in params_input:
        is_valid = client_utils.is_valid_client_ia_name_format(
            params_input.get("ia_name_format", "")
        )
        if not is_valid:
            errors.append(build_error("ia_name_format", 
                constants.INVALID_CLIENT_IA_NAME_FORMAT_MESSAGE))

    check_errors_and_return(errors)

@event.listens_for(Client, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Event hook method that fires before insert 
    to check if params are valid for inserting a single client
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value

    errors = []

    if "name" in params_input:
        is_valid, message = client_utils.is_valid_client_name(
            connection, params_input.get("name", ""), params_input.get("id", "")
        )
        if not is_valid:
            errors.append(build_error("name", message))

    if "status" in params_input:
        is_valid = client_utils.is_valid_client_status(params_input.get("status", ""))
        if not is_valid:
            errors.append(build_error("status", constants.INVALID_CLIENT_STATUS_MESSAGE))

    if "contracted_users" in params_input:
        is_valid, message = utils.is_valid_int(
            params_input.get("contracted_users", "")
        )
        if not is_valid:
            errors.append(build_error("contracted_users", message))

    if "active_inactive_date" in params_input:
        is_valid, date_obj = utils.is_valid_date(
            params_input.get("active_inactive_date", "")
        )
        if not is_valid:
            errors.append(build_error("active_inactive_date", constants.INVALID_DATE_MESSAGE))

    if "ia_name_format" in params_input:
        is_valid = client_utils.is_valid_client_ia_name_format(
            params_input.get("ia_name_format", "")
        )
        if not is_valid:
            errors.append(build_error("ia_name_format", 
                constants.INVALID_CLIENT_IA_NAME_FORMAT_MESSAGE))

    check_errors_and_return(errors)


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
