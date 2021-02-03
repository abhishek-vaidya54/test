"""
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
            Norberto Fernandez

CLASSIFICATION: 
            Highly Sensitive

    **** Add Contributors name if you have contributed to this file ****
*********************************************************************************
"""

# Standard Library Import
import datetime
import copy
import json

# Third Party Import
from sqlalchemy import (
    ForeignKey,
    PrimaryKeyConstraint,
    UniqueConstraint,
    Column,
    String,
    Integer,
    DateTime,
    Float,
    Boolean,
    Enum,
    event,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import TIME

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
from sat_orm.pipeline_orm.utilities import warehouse_utils
from sat_orm.pipeline_orm.utilities import client_utils
from sat_orm.pipeline_orm.utilities import utils
import sat_orm.constants as constants


class Warehouse(Base):
    __tablename__ = "warehouse"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=True)
    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    app_restart_at = Column(
        TIME(),
        nullable=True,
    )
    prefered_timezone = Column(String(100), server_default="UTC", nullable=False)
    algo_version = Column(Integer, nullable=True)
    display_names = Column(Boolean, nullable=False)
    utc_op_day_start = Column(String(45), nullable=False)
    week_start = Column(String(45), nullable=False)
    update_engagement = Column(Boolean, nullable=False)
    standard_score = Column(Float, nullable=True)
    min_safety_score = Column(Float, nullable=True)
    max_safety_score = Column(Float, nullable=True)
    first_quarter_safety_score = Column(Float, nullable=True)
    median_safety_score = Column(Float, nullable=True)
    third_quarter_safety_score = Column(Float, nullable=True)

    number_of_user_allocated = Column(Integer, nullable=True)
    city = Column(String(30), nullable=True)
    state = Column(String(30), nullable=True)
    country = Column(String(30), nullable=True)
    industry = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    lat_direction = Column(
        Enum("N", "S", "E", "W"),
        nullable=True,
        default="N",
    )
    long_direction = Column(
        Enum("N", "S", "E", "W"),
        nullable=True,
        default="N",
    )

    # Table Constraints
    PrimaryKeyConstraint("id")

    # Table relationships
    client = relationship("Client", back_populates="warehouses", uselist=False)
    industrial_athletes = relationship("IndustrialAthlete", back_populates="warehouse")
    job_functions = relationship("JobFunction", back_populates="warehouse")
    shifts = relationship("Shifts", back_populates="warehouse")

    @validates("client_id")
    def validate_client_id(self, key, client_id):
        if client_id == None:
            raise Exception("client_id cannot be Null")
        else:
            return client_id

    @validates("name")
    def validate_name(self, key, name):
        if name == None:
            raise Exception("name cannot be Null")
        else:
            return name

    @validates("prefered_timezone")
    def validate_prefered_timezone(self, key, prefered_timezone):
        if prefered_timezone == None:
            raise Exception("prefered_timezone cannot be Null")
        else:
            return prefered_timezone

    @validates("display_names")
    def validate_display_names(self, key, display_names):
        if display_names == None:
            raise Exception("display_names cannot be Null")
        else:
            return display_names

    @validates("update_engagement")
    def validate_update_engagement(self, key, update_engagement):
        if update_engagement == None:
            raise Exception("update_engagement cannot be Null")
        else:
            return update_engagement

    def as_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "name": self.name,
            "location": self.location,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
            "prefered_timezone": self.prefered_timezone,
            "algo_version": self.algo_version,
            "display_names": self.display_names,
            "utc_op_day_start": self.utc_op_day_start,
            "week_start": self.week_start,
            "update_engagement": self.update_engagement,
            "number_of_user_allocated": self.number_of_user_allocated,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "industry": self.industry,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "lat_direction": self.lat_direction,
            "long_direction": self.long_direction,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(Warehouse, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Event hook method that fires before insert
    to check if params are valid for inserting a single warehouse
    """

    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    client_id = params_input.get("client_id", "")
    name = params_input.get("name", "")
    number_of_user_allocated = (
        target.number_of_user_allocated if target.number_of_user_allocated else ""
    )
    industry = target.industry if target.industry else ""

    is_valid, message = utils.is_valid_string(name)
    if not is_valid:
        errors.append(utils.build_error("name", message))

    is_valid = client_utils.is_valid_client_id(connection, client_id)
    if not is_valid:
        errors.append(
            utils.build_error("client_id", constants.INVALID_CLIENT_ID_MESSAGE)
        )

    is_valid, message = utils.is_valid_string(industry)
    if not is_valid:
        errors.append(utils.build_error("industry", message))

    if number_of_user_allocated:
        is_valid, message = utils.is_valid_int(number_of_user_allocated)
        if not is_valid:
            errors.append(utils.build_error("number_of_user_allocated", message))

    for key in ["city", "state", "country"]:
        if getattr(target, key, None) is not "":
            is_valid, message = utils.is_valid_string(getattr(target, key, ""))
            if not is_valid:
                errors.append(utils.build_error(key, message))

    for key in ["latitude", "longitude"]:
        if getattr(target, key, None) is not None:
            is_valid = warehouse_utils.is_valid_lat_long(key, getattr(target, key, ""))
            if not is_valid:
                errors.append(
                    utils.build_error(key, constants.INVALID_LAT_LONG_MESSAGE[key])
                )

    for key in ["lat_direction", "long_direction"]:
        if getattr(target, key, None) is not None:
            is_valid = warehouse_utils.is_valid_lat_long_direction(
                getattr(target, key, "")
            )
            if not is_valid:
                errors.append(
                    utils.build_error(
                        key, key + constants.INVALID_LAT_LONG_DIRECTION_MESSAGE
                    )
                )

    utils.check_errors_and_return(errors)


@event.listens_for(Warehouse, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Event hook method that fires before update
    to check if params are valid for updating a single warehouse
    """

    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    is_valid = warehouse_utils.is_valid_warehouse_id(
        connection, params_input.get("id", "")
    )
    if not is_valid:
        errors.append(utils.build_error("id", constants.MISSING_ID_MESSAGE))

    if "name" in params_input:
        is_valid, message = utils.is_valid_string(params_input.get("name", ""))
        if not is_valid:
            errors.append(utils.build_error("name", message))

    if "client_id" in params_input:
        is_valid = client_utils.is_valid_client_id(
            connection, params_input.get("client_id", "")
        )
        if not is_valid:
            errors.append(
                utils.build_error("client_id", constants.INVALID_CLIENT_ID_MESSAGE)
            )

    if getattr(target, "industry", ""):
        is_valid, message = utils.is_valid_string(getattr(target, "industry"))
        if not is_valid:
            errors.append(utils.build_error("industry", message))

    if getattr(target, "number_of_user_allocated", ""):
        is_valid, message = utils.is_valid_int(
            params_input.get("number_of_user_allocated", "")
        )
        if not is_valid:
            errors.append(utils.build_error("number_of_user_allocated", message))

    for key in ["city", "state", "country"]:
        if getattr(target, key, None) is not None:
            is_valid, message = utils.is_valid_string(getattr(target, key))
            if not is_valid:
                errors.append(utils.build_error(key, message))

    for key in ["latitude", "longitude"]:
        if getattr(target, key, None) is not None:
            is_valid = warehouse_utils.is_valid_lat_long(key, getattr(target, key, ""))
            if not is_valid:
                errors.append(
                    utils.build_error(key, constants.INVALID_LAT_LONG_MESSAGE[key])
                )

    for key in ["lat_direction", "long_direction"]:
        if getattr(target, key, None) is not None:
            is_valid = warehouse_utils.is_valid_lat_long_direction(
                getattr(target, key, "")
            )
            if not is_valid:
                errors.append(
                    utils.build_error(
                        key, key + constants.INVALID_LAT_LONG_DIRECTION_MESSAGE
                    )
                )

    utils.check_errors_and_return(errors)
