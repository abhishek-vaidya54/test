"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
            Hashmat Ibrahimi

CLASSIFICATION: 
            Highly Sensitive 

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
"""

# Standard Library Imports
import datetime


# Third Party Imports
from sqlalchemy import ForeignKey, Column, Integer, DateTime, Text, String, event
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import TINYINT

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import shift_utils
from sat_orm.pipeline_orm.utilities import job_function_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return
from sat_orm.pipeline_orm.utilities import external_admin_user_utils


class Shifts(Base):
    __tablename__ = "shifts"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    name = Column(String(255), nullable=False)
    shift_start = Column(DateTime, nullable=False)
    shift_end = Column(DateTime, nullable=False)
    shift_manager_id = Column(
        Integer, ForeignKey("external_admin_user.id"), nullable=True
    )
    description = Column(Text, nullable=True)
    color = Column(String(255), nullable=True)
    override_settings = Column(TINYINT(1), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    # Table Relationships
    industrial_athletes = relationship(
        "IndustrialAthlete", back_populates="shifts")
    warehouse = relationship(
        "Warehouse", back_populates="shifts", uselist=False)
    external_admin_user = relationship(
        "ExternalAdminUser",  back_populates="shifts"
    )

    @validates("warehouse_id")
    def validate_warehouse_id(self, key, warehouse_id):
        if warehouse_id == None:
            raise Exception("warehouse_id cannot be Null")
        else:
            return warehouse_id

    @validates("name")
    def validate_name(self, key, name):
        if name == None:
            raise Exception("name cannot be Null")
        else:
            return name

    @validates("shift_start")
    def validate_shift_start(self, key, shift_start):
        if shift_start == None:
            raise Exception("shift_start cannot be Null")
        else:
            return shift_start

    @validates("shift_end")
    def validate_shift_end(self, key, shift_end):
        if shift_end == None:
            raise Exception("shift_end cannot be Null")
        else:
            return shift_end

    def as_dict(self):
        return {
            "id": self.id,
            "warehouseId": self.warehouse_id,
            "name": self.name,
            "shiftStart": self.shift_start,
            "shiftEnd": self.shift_end,
            "color": self.color,
            "override_settings": self.override_settings,
            "description": self.description,
            "external_admin_user": self.external_admin_user,
            "shift_manager_id": self.shift_manager_id,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(Shifts, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Event hook to check if params are valid for adding a single shift
    """
    param_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            param_input[key] = value
    errors = []
    # Name
    is_valid, message = shift_utils.is_valid_shift_name(
        connection, param_input.get("name", ""), param_input.get("id", ""), param_input.get("warehouseId", ""))


    if not is_valid:
        errors.append(build_error("name", message))
    # Warehouse ID
    is_valid = shift_utils.is_valid_warehouse(
        connection, param_input.get("warehouseId", "")
    )
    if not is_valid:
        errors.append(
            build_error("warehouse_id", constants.INVALID_WAREHOUSE_ID_MESSAGE)
        )
    # Shift start
    is_valid, message = shift_utils.is_valid_time(
        param_input.get("shiftStart", ""))
    if not is_valid:
        errors.append(build_error(
            "shift_start", constants.INVALID_DATE_MESSAGE))
    # Shift end
    is_valid, message = shift_utils.is_valid_time(
        param_input.get("shiftEnd", ""))
    if not is_valid:
        errors.append(build_error("shift_end", constants.INVALID_DATE_MESSAGE))

    # Shift Manager

    is_valid = external_admin_user_utils.is_valid_user_id(
        connection, param_input.get("shift_manager_id")
    )
    if not is_valid:
        errors.append(
            build_error(
                "external_admin_user_id", constants.INVALID_PARAM_SHIFT_MANAGER_MESSAGE
            )
        )
    check_errors_and_return(errors)


@event.listens_for(Shifts, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Event hook to check if params are valid for updating a single shift
    """
    param_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            param_input[key] = value

    errors = []

    # Name
    if "name" in param_input:
        is_valid, message = shift_utils.is_valid_shift_name(
            connection, param_input.get("name", ""), param_input.get("id", ""), param_input.get("warehouseId", ""))


        if not is_valid:
            errors.append(build_error("name", message))
    # Warehouse ID
    if "warehouseId" in param_input:
        is_valid = shift_utils.is_valid_warehouse(
            connection, param_input.get("warehouseId", "")
        )
        if not is_valid:
            errors.append(
                build_error("warehouse_id",
                            constants.INVALID_WAREHOUSE_ID_MESSAGE)
            )
    # Shift start
    if "shiftStart" in param_input:
        is_valid, message = shift_utils.is_valid_time(
            param_input.get("shiftStart", ""))
        if not is_valid:
            errors.append(build_error(
                "shift_start", constants.INVALID_DATE_MESSAGE))
    # Shift end
    if "shiftEnd" in param_input:
        is_valid, message = shift_utils.is_valid_time(
            param_input.get("shiftEnd", ""))
        if not is_valid:
            errors.append(build_error(
                "shift_end", constants.INVALID_DATE_MESSAGE))
        # Shift Manager
    if "shift_manager_id" in param_input:
        is_valid = external_admin_user_utils.is_valid_user_id(
            connection, param_input.get("shift_manager_id")
        )
        if not is_valid:
            errors.append(
                build_error(
                    "external_admin_user_id", constants.INVALID_PARAM_SHIFT_MANAGER_MESSAGE
                )
            )

    check_errors_and_return(errors)
