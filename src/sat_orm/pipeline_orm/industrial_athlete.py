"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
"""

# Standard Library Imports
import datetime


# Third Party Imports
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    desc,
    event,
)
from sqlalchemy.orm import relationship, validates


# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import ia_utils, client_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return
from utilities.common import utils


class IndustrialAthlete(Base):
    __tablename__ = "industrial_athlete"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    gender = Column(String(1), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=False)
    schedule = Column(String(255), nullable=True)
    shift_per_week = Column(Integer, nullable=False, default=0)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    prior_back_injuries = Column(String(255), nullable=True)
    hire_date = Column(DateTime, default=datetime.date.today(), nullable=True)
    termination_date = Column(DateTime, nullable=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    trained = Column(Boolean, nullable=True, default=False)
    harness_provided = Column(Boolean, nullable=True, default=False)

    job_function_id = Column(Integer, ForeignKey("job_function.id"), nullable=False)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    setting_id = Column(Integer, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    job_function_change_date = Column(DateTime, nullable=True)
    gender_change_date = Column(DateTime, nullable=True)
    # is_active = Column(Boolean, nullable=True, server_default=None)

    # Table Relationships
    client = relationship("Client", back_populates="industrial_athletes", uselist=False)
    warehouse = relationship(
        "Warehouse", back_populates="industrial_athletes", uselist=False
    )
    shifts = relationship("Shifts", back_populates="industrial_athletes", uselist=False)
    job_function = relationship(
        "JobFunction", back_populates="industrial_athletes", uselist=False
    )
    groups = relationship("Groups", back_populates="industrial_athletes", uselist=False)

    @validates("client_id")
    def validate_client_id(self, key, client_id):
        if client_id == None:
            raise Exception("client_id cannot be Null")
        else:
            return client_id

    @validates("gender")
    def validate_gender(self, key, gender):
        if gender == None:
            raise Exception("gender cannot be Null")
        else:
            return gender

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if first_name == None:
            raise Exception("first_name cannot be Null")
        else:
            return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if last_name == None:
            raise Exception("last_name cannot be Null")
        else:
            return last_name

    @validates("shift_per_week")
    def validate_shift_per_week(self, key, shift_per_week):
        if shift_per_week == None:
            utils.return_error_response("shift_per_week cannot be Null")
        elif shift_per_week < 0:
            utils.return_error_response("shift_per_week cannot be negative")
        else:
            return shift_per_week

    @validates("external_id")
    def validate_external_id(self, key, external_id):
        if external_id == None:
            raise Exception("external_id cannot be Null")
        else:
            return external_id

    @validates("warehouse_id")
    def validate_warehouse_id(self, key, warehouse_id):
        if warehouse_id == None:
            raise Exception("warehouse_id cannot be Null")
        else:
            return warehouse_id

    @validates("shift_id")
    def validate_shift_id(self, key, shift_id):
        if shift_id == None:
            raise Exception("shift_id cannot be Null")
        else:
            return shift_id

    @validates("job_function_id")
    def validate_job_function_id(self, key, job_function_id):
        if job_function_id == None:
            raise Exception("job_function_id cannot be Null")
        else:
            return job_function_id

    def as_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "externalId": self.external_id,
            "shift_per_week": self.shift_per_week,
            "sex": self.gender,
            "shiftId": self.shift_id,
            "jobFunctionId": self.job_function_id,
            "clientId": self.client_id,
            "warehouseId": self.warehouse_id,
            "hireDate": self.hire_date,
            "terminationDate": self.termination_date,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    def __repr__(self):
        return str(self.as_dict())

    def __len__(self):
        return len(self.as_dict())


@event.listens_for(IndustrialAthlete, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single athlete
    Input:
        param_input: json containing data to be added for a single athlete.
        warehouse_id: warehouse ID to validate job function
    """
    param_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            param_input[key] = value
    errors = []

    is_valid, message = ia_utils.is_valid_ia_first_last_name(
        connection, param_input.get("firstName", ""), "First Name", target.client_id
    )
    if not is_valid:
        errors.append(build_error("firstName", message))

    is_valid, message = ia_utils.is_valid_ia_first_last_name(
        connection, param_input.get("lastName", ""), "Last Name", target.client_id
    )
    if not is_valid:
        errors.append(build_error("lastName", message))

    is_valid, message = ia_utils.is_valid_external_id(
        connection,
        param_input.get("externalId", ""),
        param_input.get("warehouseId"),
        param_input.get("hireDate"),
    )
    if not is_valid:
        errors.append(build_error("externalId", message))

    is_valid = param_input.get("sex", "") in ("m", "f")
    if not is_valid:
        errors.append(build_error("sex", constants.INVALID_PARAM_SEX_MESSAGE))

    is_valid = client_utils.is_valid_client_id(
        connection, param_input.get("clientId", "")
    )
    if not is_valid:
        errors.append(
            utils.build_error("clientId", constants.INVALID_CLIENT_ID_MESSAGE)
        )

    is_valid = ia_utils.is_valid_warehouse(
        connection, param_input.get("warehouseId", ""), target.client_id
    )
    if not is_valid:
        errors.append(build_error("warehouseId", constants.INVALID_WAREHOUSE_MESSAGE))

    is_valid = ia_utils.is_valid_shift(
        connection, param_input.get("shiftId", ""), target.warehouse_id
    )
    if not is_valid:
        errors.append(build_error("shiftId", constants.INVALID_SHIFT_MESSAGE))

    is_valid = ia_utils.is_valid_job_function(
        connection, param_input.get("jobFunctionId", ""), target.warehouse_id
    )
    if not is_valid:
        errors.append(
            build_error("jobFunctionId", constants.INVALID_JOB_FUNCTION_MESSAGE)
        )

    is_valid, date_obj = utils.is_valid_date(param_input.get("hireDate", ""))
    if not is_valid:
        errors.append(build_error("hireDate", constants.INVALID_DATE_MESSAGE))

    check_errors_and_return(errors)


@event.listens_for(IndustrialAthlete, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Helper method to check if params are valid for updating a single athlete
    Input:
        param_input: json containing data to be updated for a single athlete.
                        id field MUST be inside.
        warehouse_id: warehouse ID to validate job function
    Output:
        Return [True, None] if all params are valid.
        Returns [False, Errors] if there are params which are not valid
    """
    key_mappings = {
        "firstName": "first_name",
        "lastName": "last_name",
        "externalId": "external_id",
        "sex": "gender",
        "clientId": "client_id",
        "warehouseId": "warehouse_id",
        "shiftId": "shift_id",
        "jobFunctionId": "job_function_id",
        "hireDate": "hire_date",
        "terminationDate": "termination_date",
    }

    # Athlete ID is required
    ia = connection.execute(
        "SELECT * FROM industrial_athlete WHERE id={}".format(target.id)
    ).fetchone()

    param_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            if getattr(ia, key_mappings.get(key, key), value) != value:
                param_input[key] = value

    errors = []

    if "firstName" in param_input:
        is_valid, message = ia_utils.is_valid_ia_first_last_name(
            connection, param_input.get("firstName", ""), "First Name", ia.client_id
        )
        if not is_valid:
            errors.append(build_error("firstName", message))

    if "lastName" in param_input:
        is_valid, message = ia_utils.is_valid_ia_first_last_name(
            connection, param_input.get("lastName", ""), "Last Name", ia.client_id
        )
        if not is_valid:
            errors.append(build_error("lastName", message))

    if "externalId" in param_input:
        is_valid, message = ia_utils.is_valid_external_id(
            connection,
            param_input.get("externalId", ""),
            ia.warehouse_id,
            param_input.get("hireDate", ""),
            ia,
            existing_ia_id=param_input.get("id"),
        )
        if not is_valid:
            errors.append(build_error("externalId", message))

    if "sex" in param_input:
        is_valid = param_input.get("sex", "") in ("m", "f")
        if not is_valid:
            errors.append(build_error("sex", constants.INVALID_PARAM_SEX_MESSAGE))

    if "clientId" in param_input:
        is_valid = client_utils.is_valid_client_id(
            connection, param_input.get("clientId", "")
        )
        if not is_valid:
            errors.append(
                utils.build_error("clientId", constants.INVALID_CLIENT_ID_MESSAGE)
            )

    if "warehouseId" in param_input:
        is_valid = ia_utils.is_valid_warehouse(
            connection, param_input.get("warehouseId", ""), ia.client_id
        )
        if not is_valid:
            errors.append(
                build_error("warehouseId", constants.INVALID_WAREHOUSE_MESSAGE)
            )

    if "shiftId" in param_input:
        is_valid = ia_utils.is_valid_shift(
            connection,
            param_input.get("shiftId", ""),
            param_input.get("warehouseId", ia.warehouse_id),
        )
        if not is_valid:
            errors.append(build_error("shiftId", constants.INVALID_SHIFT_MESSAGE))

    if "jobFunctionId" in param_input:
        is_valid = ia_utils.is_valid_job_function(
            connection,
            param_input.get("jobFunctionId", ""),
            param_input.get("warehouseId", ia.warehouse_id),
        )
        if not is_valid:
            errors.append(
                build_error("jobFunctionId", constants.INVALID_JOB_FUNCTION_MESSAGE)
            )

    if "hireDate" in param_input:
        is_valid, date_obj = utils.is_valid_date(param_input.get("hireDate", ""))
        if not is_valid:
            errors.append(build_error("hireDate", constants.INVALID_DATE_MESSAGE))

    if "terminationDate" in param_input:
        is_valid, date_obj = utils.is_valid_date(param_input.get("terminationDate", ""))
        if not is_valid:
            errors.append(
                build_error("terminationDate", constants.INVALID_DATE_MESSAGE)
            )

    check_errors_and_return(errors)


def get_all_athletes(session):
    """
    Generic select * from industrial_athlete where column = value for value in filter_args
    """
    return session.query(IndustrialAthlete).all()


def dockv5_getAthletes_select_by_client_warehouse_not_terminated(
    session, client_id, warehouse_id
):
    """
    Implements the below query in the DockV5-API getAthletes lambda:
    SELECT * FROM industrial_athlete WHERE client_id= %s AND warehouse_id= %s AND termination_date is NULL;', (client_id, warehouse_id)
    """
    return (
        session.query(IndustrialAthlete)
        .filter(
            IndustrialAthlete.client_id == client_id,
            IndustrialAthlete.warehouse_id == warehouse_id,
            IndustrialAthlete.termination_date.isnot(None),
        )
        .all()
    )


def dockv5_getEngagement_select_by_id(session, id):
    """
    Implements the below query in the DockV5-API getEngagement lambda:
    'SELECT * FROM industrial_athlete WHERE id=%s LIMIT 1',(athlete_id)
    """
    return session.query(IndustrialAthlete).filter(IndustrialAthlete.id == id).first()


def dockv5_getUpdatedAthletes_select_group_id(session, client_id, warehouse_id):
    """
    Implements the below query in the DockV5-API getUpdatedAthletes lambda:
    select group_id from industrial_athlete where client_id = %s and warehouse_id = %s)
    """
    return (
        session.query(IndustrialAthlete.group_id)
        .filter(
            IndustrialAthlete.client_id == client_id,
            IndustrialAthlete.warehouse_id == warehouse_id,
        )
        .all()
    )


def dockv5_getUpdatedAthletes_select_id(session, client_id, warehouse_id):
    """
    Implements the below query in DockV5-API getUpdatedAthletes lambda:
    select id from industrial_athlete where client_id = %s and warehouse_id = %s
    """
    return (
        session.query(IndustrialAthlete.id)
        .filter(
            IndustrialAthlete.client_id == client_id,
            IndustrialAthlete.warehouse_id == warehouse_id,
        )
        .all()
    )


def dockv5_getUpdatedAthletes_select_by_db_modified(session, last_checked_timestamp):
    """
    Implements the below query in DockV5-API getUpdatedAthletes lambda:
    select * from industrial_athlete where db_modified_at > %s order by db_modified_at DESC;
    """
    return (
        session.query(IndustrialAthlete)
        .filter(IndustrialAthlete.db_modified_at > last_checked_timestamp)
        .order_by(IndustrialAthlete.db_modified_at)
        .all()
    )


# TODO ''


def dockv5_getUpdatedAthletes_select_by_client_warehouse_db_modified(
    session, client_id, warehouse_id, last_athlete_check
):
    """
    Implements the below query in DockV5-API getUpdatedAthletes lambda:
    'select * from industrial_athlete where client_id = %s and warehouse_id = %s and db_modified_at > %s order by db_modified_at DESC'
    """
    return (
        session.query(IndustrialAthlete)
        .filter(
            IndustrialAthlete.client_id == client_id,
            IndustrialAthlete.warehouse_id == warehouse_id,
            IndustrialAthlete.db_modified_at > last_athlete_check,
        )
        .order_by(desc(IndustrialAthlete.db_modified_at))
    )

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
