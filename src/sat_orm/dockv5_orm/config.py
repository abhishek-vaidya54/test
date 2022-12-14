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

# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, desc, event
from sqlalchemy.dialects.mysql import insert

# Local Application Imports
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return
import sat_orm.constants as constants
from sat_orm.dockv5_orm.dockv5_base import Base
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import ia_utils, client_utils
from sat_orm.dockv5_orm.utilities import dock_utils


class Config(Base):
    __tablename__ = "config"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    dock_id = Column(String(45), nullable=True, unique=True)
    dock_imei = Column(String(45), nullable=True)
    serial_number = Column(String(45), nullable=True)
    client_id = Column(Integer, nullable=True)
    warehouse_id = Column(Integer, nullable=True)
    deployment_stage = Column(String(45), default="DEV", nullable=True)
    barcode_regex = Column(String(45), nullable=True)
    firmware_version = Column(Integer, nullable=True)
    description = Column(String(500), nullable=True)
    firmware_group_id = Column(Integer, ForeignKey("firmware_group.id"), nullable=False)

    # Relationships
    firmware_group = relationship("FirmwareGroup", back_populates="configs")

    @validates("client_id")
    def validate_client_id(self, key, client_id):
        if client_id == None:
            raise Exception("client_id cannot be Null")
        else:
            assert True
            return client_id

    # @validates('dock_id')
    # def validate_dock_id(self, key, dock_id):
    #     if dock_id == None:
    #         raise Exception('dock_id cannot be Null')
    # #     else:
    # #         dock_id_length = 12
    # #         assert isinstance(dock_id, str)
    # #         assert len(dock_id) == dock_id_length
    # #         return dock_id

    @validates("warehouse_id")
    def validate_warehouse_id(self, key, warehouse_id):
        if warehouse_id == None:
            raise Exception("warehouse_id cannot be Null")
        else:
            return warehouse_id

    @validates("barcode_regex")
    def validate_barcode_regex(self, key, barcode_regex):
        if barcode_regex == "":
            return None
        else:
            return barcode_regex

    # @validates('deployment_stage')
    # def validate_deployment_stage(self, key, deployment_stage):
    #     if deployment_stage == None:
    #         raise Exception('deployment_stage cannot be Null')
    #     elif deployment_stage not in ['dev', 'prod']:
    #         raise Exception('deployment_stage can only be [dev,prod]')
    #     else:
    #         return deployment_stage

    def as_dict(self):
        return {
            "id": self.id,
            "dock_id": self.dock_id,
            "dock_imei": self.dock_imei,
            "serial_number": self.serial_number,
            "client_id": self.client_id,
            "warehouse_id": self.warehouse_id,
            "deployment_stage": self.deployment_stage,
            "barcode_regex": self.barcode_regex,
            "firmware_version": self.firmware_version,
            "description": self.description,
        }

    def __repr__(self):
        return str(self.as_dict())


def insert_or_update(session, data):
    """
    Description
        checks to see if dock_id is in table,
        if it is, then only update the none primary key items.
        else insert a new row.

    params
        session: sqlalchemy.orm.session.Session
        data: {key: value} dictionary

    return
        Does not return anything, however does commit to database
    """
    data.pop("phase", None)  # removes phase if in data
    dock_id = data["dock_id"]
    dock_in_table = session.query(Config).filter_by(dock_id=data["dock_id"]).first()
    if dock_in_table:
        data.pop("dock_id", None)  # removes dock_id if in data
        session.query(Config).filter_by(dock_id=dock_id).update(data)
        session.commit()
    else:
        config = Config(
            dock_id=data.get("dock_id", None),
            client_id=data.get("client_id", None),
            warehouse_id=data.get("warehouse_id", None),
            deployment_stage=data.get("deployment_stage", "dev"),
            barcode_regex=data.get("barcode_regex", None),
            firmware_version=data.get("firmware_version", None),
            description=data.get("description", None),
            dock_imei=data.get("dock_imei", None),
            serial_number=data.get("serial_number", None),
        )

        session.add(config)
        session.commit()


@event.listens_for(Config, "before_insert")
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

    # DockID
    if "dock_id" in params_input:
        is_valid, message = dock_utils.is_valid_dock_id(
            connection, params_input.get("dock_id", "")
        )
        if not is_valid:
            errors.append(build_error("dockId", message))
    # Deployment Phase
    if "deployment_stage" in params_input:
        is_valid, message = dock_utils.is_valid_dock_deployment_stage(
            params_input.get("deployment_stage", "")
        )
        if not is_valid:
            errors.append(build_error("deploymentStage", message))

    # Client and warehouse
    if "warehouse_id" in params_input:
        is_valid = ia_utils.is_valid_warehouse(
            connection,
            params_input.get("warehouse_id", ""),
            params_input.get("client_id", ""),
        )
        if not is_valid:
            errors.append(
                build_error("warehouseId", constants.INVALID_WAREHOUSE_CLIENT_MESSAGE)
            )

    check_errors_and_return(errors)


@event.listens_for(Config, "before_update")
def validate_before_update(mapper, connection, target):
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
    # phase = params_input.get("phase", "")
    # deployment_stage = params_input.get("deployment_stage", "")

    # Warehouse ID
    if "warehouse_id" in params_input:
        is_valid = ia_utils.is_valid_warehouse(
            connection,
            params_input.get("warehouse_id", ""),
            params_input.get("client_id", ""),
        )
        if not is_valid:
            errors.append(
                build_error("warehouseId", constants.INVALID_WAREHOUSE_CLIENT_MESSAGE)
            )
    # Deployment Phase
    if "deployment_stage" in params_input:
        is_valid, message = dock_utils.is_valid_dock_deployment_stage(
            params_input.get("deployment_stage", "")
        )
        if not is_valid:
            errors.append(build_error("deploymentStage", message))

    check_errors_and_return(errors)
