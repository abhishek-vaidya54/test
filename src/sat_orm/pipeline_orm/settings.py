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


# Third Party Library Imports
from sqlalchemy import Column, Integer, String, JSON, DateTime, event, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import validates

# Local Application Imports
from sqlalchemy.orm import relationship
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import external_admin_user_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return
from sat_orm.pipeline_orm.utilities import setting_utils


class Setting(Base):
    __tablename__ = "settings"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_type = Column(String(45), nullable=False)
    target_id = Column(Integer, nullable=False)
    value = Column(JSON, nullable=True, server_default=None)
    db_created_by = Column(
        Integer, ForeignKey("external_admin_user.id"))
    db_created_at = Column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationship
    external_admin_user = relationship(
        "ExternalAdminUser", uselist=False
    )

    @validates("target_type")
    def validate_target_type(self, key, target_type):
        if target_type is None:
            raise Exception("target_type cannot be Null")
        else:
            return target_type

    @validates("target_id")
    def validate_target_id(self, key, target_id):
        if target_id is None:
            raise Exception("target_id cannot be Null")
        else:
            return target_id

    def as_dict(self):
        return {
            "id": self.id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "value": self.value,
            "db_created_by": self.db_created_by,
            "db_created_at": self.db_created_at,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(Setting, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single setting
    Input:
        params_input: json containing data to be added for a single setting.
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    target_type = params_input.get("target_type", "")
    target_id = params_input.get("target_id", 0)
    value = params_input.get("value", {})
    db_created_by = params_input.get("db_created_by", None)

    is_valid = setting_utils.is_valid_target_type(target_type)
    if not is_valid:
        errors.append(build_error("target_type", constants.INVALID_TARGET_TYPE_MESSAGE))

    is_valid, message = setting_utils.is_valid_target_id(
        connection, target_type, target_id
    )
    if not is_valid:
        errors.append(build_error("target_id", message))

    is_valid, message = setting_utils.is_valid_value_obj(value)
    if not is_valid:
        errors.append(build_error("value", message))

    is_valid = external_admin_user_utils.is_valid_user_id(
        connection, db_created_by
    )
    if not is_valid:
        errors.append(
            build_error(
                "db_created_by", constants.INVALID_PARAM_USERNAME_MESSAGE
            )
        )

    check_errors_and_return(errors)