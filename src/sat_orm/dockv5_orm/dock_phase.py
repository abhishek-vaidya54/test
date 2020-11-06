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
import copy
import json

# Third Party Imports
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    Boolean,
    event,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import text

# Local Application Imports
from sat_orm.dockv5_orm.dockv5_base import Base
from sat_orm.dockv5_orm.config import Config
from sat_orm.pipeline import Warehouse, Client
import sat_orm.constants as constants
from sat_orm.dockv5_orm.utilities import dock_utils
from sat_orm.pipeline_orm.utilities import ia_utils


class DockPhase(Base):
    __tablename__ = "dock_phase"

    # Table inputs
    id = Column(Integer, primary_key=True, autoincrement=True)
    dock_id = Column(String, ForeignKey("config.dock_id"), nullable=False)
    description = Column(String(255), nullable=False)

    warehouse_id = Column(Integer, ForeignKey(Warehouse.id), nullable=False)
    warehouse = relationship(Warehouse, foreign_keys=warehouse_id, backref="dock_phase")

    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    client = relationship(Client, foreign_keys=client_id, backref="dock_phase")
    dock_firmware = Column(Boolean, nullable=True, default=False)
    dock_firmware_version = Column(String(10), nullable=False)
    timestamp = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    phase = Column(
        Enum("DEPLOYED", "NOT DEPLOYED", "MAINTENANCE"),
        nullable=False,
        default="NOT DEPLOYED",
    )
    phase_date = Column(DateTime, nullable=True)
    deployment_stage = Column(Enum("DEV", "PROD"), nullable=False, default="dev")
    # config = relationship("Config", back_populates="dock_phase")
    # configs = relationship("Config", back_populates="dock_phases")

    @validates("dock_id")
    def validate_dock_id(self, key, dock_id):
        if dock_id == None:
            raise Exception("dock_id cannot be Null")
        else:
            return dock_id

    @validates("timestamp")
    def validate_timestamp(self, key, timestamp):
        if timestamp == None:
            raise Exception("timestamp cannot be Null")
        else:
            return timestamp

    @validates("phase")
    def validate_phase(self, key, phase):
        if phase == None:
            raise Exception("phase cannot be Null")
        else:
            return phase

    @validates("deployment_stage")
    def validate_deployment_stage(self, key, deployment_stage):
        if deployment_stage == None:
            raise Exception("deployment_stage cannot be Null")
        else:
            return deployment_stage

    def as_dict(self):
        return {
            "id": self.id,
            "dock_id": self.dock_id,
            "client_id": self.client_id,
            "warehouse_id": self.warehouse_id,
            "phase": self.phase,
            "phase_date": self.phase_date,
            "deployment_stage": self.deployment_stage,
            "dock_firmware_version": self.dock_firmware_version,
            "description": self.description,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(DockPhase, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single athlete
    Input:
        params_input: json containing data to be added for a single athlete.
        warehouse_id: warehouse ID to validate job function
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    dock_id = params_input.get("dock_id", "")
    client_id = params_input.get("client_id", "")
    warehouse_id = params_input.get("warehouse_id", "")
    phase = params_input.get("phase", "")
    phase_date = params_input.get("phase_date", "")
    deployment_stage = params_input.get("deployment_stage", "")
    dock_firmware_version = params_input.get("dock_firmware_version", "")
    description = params_input.get("description", "")

    is_valid = dock_utils.is_non_empty_string(dock_id)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "dock_id"
        error["reason"] = constants.EMPTY_STRING_ERROR_MESSAGE
        errors.append(error)

    is_valid = ia_utils.is_valid_client(connection, client_id)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "client_id"
        error["reason"] = constants.INVALID_CLIENT_ID_MESSAGE
        errors.append(error)

    is_valid = ia_utils.is_valid_warehouse(connection, warehouse_id)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "warehouse_id"
        error["reason"] = constants.INVALID_WAREHOUSE_ID_MESSAGE
        errors.append(error)

    is_valid = dock_utils.is_valid_dock_phase(phase)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "phase"
        error["reason"] = constants.INVALID_DOCK_PHASE_MESSAGE
        errors.append(error)

    is_valid, date_obj = ia_utils.is_valid_date(phase_date)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "phase_date"
        error["reason"] = constants.INVALID_DATE_MESSAGE
        errors.append(error)

    is_valid = dock_utils.is_valid_dock_deployment_stage(deployment_stage)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "deployment_stage"
        error["reason"] = constants.INVALID_DOCK_DEPLOYMENT_STAGE_MESSAGE
        errors.append(error)

    is_valid = dock_utils.is_valid_dock_firmware_version(dock_firmware_version)
    if not is_valid:
        error = copy.deepcopy(constants.ERROR_DATA)
        error["fieldName"] = "dock_firmware_version"
        error["reason"] = constants.INVALID_DOCK_FIRMWARE_VERSION_MESSAGE
        errors.append(error)

    if description.strip():
        is_valid, message = ia_utils.is_valid_string(description.strip())
        if not is_valid:
            error = copy.deepcopy(constants.ERROR_DATA)
            error["fieldName"] = "description"
            error["reason"] = message
            errors.append(error)

    if len(errors) > 0:
        error_response = copy.deepcopy(constants.ERROR)
        error_response["message"] = constants.INVALID_PARAMS_MESSAGE
        error_response["errors"] = errors
        raise Exception(json.dumps(error_response))


def update_phase(session, data):
    """checks to see if the phase changed, if it did,
    a new row will be added to dock_phase. If there is no dock_id,
    add the new dock_id
    """
    current_config = (
        session.query(Config).filter_by(dock_id=data.get("dock_id", None)).first()
    )
    if (
        current_config.dock_phase == None
        or data.get("phase", None) != current_config.dock_phase.phase
    ):
        dock_phase = DockPhase(
            dock_id=data.get("dock_id", None),
            phase=data.get("phase", None),
            deployment_stage=data.get("deployment_stage", None),
        )
        session.add(dock_phase)
        session.commit()
