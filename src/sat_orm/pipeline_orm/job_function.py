"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
            Hashmat Ibrahimi
            Norberto Fernandez

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
    DateTime,
    Float,
    Text,
    Boolean,
    PrimaryKeyConstraint,
    event,
    Enum,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import TINYINT

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import ia_utils
from sat_orm.pipeline_orm.utilities import job_function_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class JobFunction(Base):
    __tablename__ = "job_function"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    name = Column(String(255), nullable=False)
    package_unit = Column(
        Enum("KG", "LBS"),
        nullable=False,
        default="LBS",
    )
    max_package_mass = Column(Float, default=6.6)
    max_package_weight = Column(Integer, nullable=True)
    min_package_weight = Column(Integer, nullable=True)
    avg_package_weight = Column(Integer, nullable=True)
    lbd_indicence = Column(Boolean, nullable=True, default=False)
    lbd_indicence_rate = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    color = Column(String(255), nullable=True)
    override_settings = Column(TINYINT(1), nullable=False)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    standard_score = Column(Float)
    min_safety_score = Column(Float, nullable=True)
    max_safety_score = Column(Float, nullable=True)
    first_quarter_safety_score = Column(Float, nullable=True)
    median_safety_score = Column(Float, nullable=True)
    third_quarter_safety_score = Column(Float, nullable=True)
    settings_id = Column(Integer, ForeignKey("settings.id"), nullable=False)
    settings = relationship("Setting", foreign_keys=settings_id, backref="settings")

    # Table Constraints
    PrimaryKeyConstraint("id")

    # Table Relationships
    industrial_athletes = relationship(
        "IndustrialAthlete", back_populates="job_function"
    )
    warehouse = relationship("Warehouse", back_populates="job_functions", uselist=False)

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

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "package_unit": self.package_unit,
            "description": self.description,
            "warehouse_id": self.warehouse_id,
            "settings_id": self.settings_id,
            # "max_package_weight": self.max_package_weight,
            "max_package_mass": self.max_package_mass,
            "override_settings": self.override_settings,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(JobFunction, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid
    Return [True, None] if all params are valid.
    Returns [False, Errors] if there are params which are not valid
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    name = params_input.get("name", "")
    description = params_input.get("description", "")
    warehouse_id = params_input.get("warehouse_id", "")
    settings_id = params_input.get("settings_id", "")
    # max_package_weight = params_input.get("max_package_weight", "")
    # max_package_mass = params_input.get("max_package_mass", "")

    is_valid, message = job_function_utils.is_valid_job_function_name(
        connection,
        params_input.get("name", ""),
        params_input.get("id", ""),
        params_input.get("warehouse_id", ""),
    )
    if not is_valid:
        errors.append(build_error("name", message))

    is_valid = ia_utils.is_valid_warehouse(connection, warehouse_id)
    if not is_valid:
        errors.append(
            build_error("warehouse_id", constants.INVALID_WAREHOUSE_ID_MESSAGE)
        )

    if settings_id:
        is_valid = ia_utils.is_valid_setting(connection, settings_id)
        if not is_valid:
            errors.append(
                build_error("settings_id", constants.INVALID_SETTINGS_ID_MESSAGE)
            )

    if description:
        is_valid, message = utils.is_valid_string(description)
        if not is_valid:
            errors.append(build_error("description", message))

    # is_valid, message = utils.is_valid_float(max_package_weight)
    # if not is_valid:
    #     errors.append(build_error("max_package_weight", message))
    # is_valid, message = utils.is_valid_float(max_package_mass)
    # if not is_valid:
    #     errors.append(build_error("max_package_mass", message))

    if "package_unit" in params_input:
        is_valid = job_function_utils.is_valid_package_unit(
            params_input.get("package_unit", "")
        )
        if not is_valid:
            errors.append(
                build_error("package_unit", constants.INVALID_PACKAGE_UNITS_MESSAGE)
            )
    check_errors_and_return(errors)


@event.listens_for(JobFunction, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Helper method to check if params are valid for updating a single job_function
    Input:
        param_input: json containing data to be updated for a single job_function.
                        id field MUST be inside.
    Output:
        Return [True, None] if all params are valid.
        Returns [False, Errors] if there are params which are not valid
    """
    # Athlete ID is required
    jf = connection.execute(
        f"SELECT * FROM job_function WHERE id={target.id}"
    ).fetchone()

    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            if getattr(jf, key, value) != value:
                params_input[key] = value

    errors = []

    if "name" in params_input:
        is_valid, message = job_function_utils.is_valid_job_function_name(
            connection,
            params_input.get("name", ""),
            params_input.get("id", ""),
            params_input.get("warehouse_id", ""),
        )
        if not is_valid:
            errors.append(build_error("name", message))

    if "warehouse_id" in params_input:
        is_valid = ia_utils.is_valid_warehouse(
            connection, params_input.get("warehouse_id", "")
        )
        if not is_valid:
            errors.append(
                build_error("warehouse_id", constants.INVALID_WAREHOUSE_ID_MESSAGE)
            )

    if "settings_id" in params_input:
        is_valid = ia_utils.is_valid_setting(
            connection, params_input.get("settings_id", "")
        )
        if not is_valid:
            errors.append(
                build_error("settings_id", constants.INVALID_SETTINGS_ID_MESSAGE)
            )

    # if "description" in params_input:
    #     is_valid, message = utils.is_valid_string(params_input.get("description", ""))
    #     if not is_valid:
    #         errors.append(build_error("description", message))

    # if "max_package_weight" in params_input:
    #     is_valid, message = utils.is_valid_float(
    #         params_input.get("max_package_weight", "")
    #     )
    #     if not is_valid:
    #         errors.append(build_error("max_package_weight", message))

    # if "max_package_mass" in params_input:
    #     is_valid, message = utils.is_valid_float(
    #         params_input.get("max_package_mass", "")
    #     )
    #     if not is_valid:
    #         errors.append(build_error("max_package_mass", message))

    if "package_unit" in params_input:
        is_valid = job_function_utils.is_valid_package_unit(
            params_input.get("package_unit", "")
        )
        if not is_valid:
            errors.append(
                build_error("package_unit", constants.INVALID_PACKAGE_UNIT_MESSAGE)
            )

    check_errors_and_return(errors)
