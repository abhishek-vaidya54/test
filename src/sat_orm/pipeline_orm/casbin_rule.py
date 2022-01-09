from logging import error
from sqlalchemy import Column, String, Integer, event

import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return

from sat_orm.pipeline_orm.pipeline_base import Base


class CasbinRule(Base):
    __tablename__ = "casbin_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ptype = Column(String(255), nullable=True, default="p")
    v0 = Column(String(255), nullable=True)
    v1 = Column(String(255), nullable=True)
    v2 = Column(String(255), nullable=True)
    v3 = Column(String(255), nullable=True)
    v4 = Column(String(255), nullable=True)
    v5 = Column(String(255), nullable=True)


@event.listens_for(CasbinRule, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Event hook method that fires before insert to check if
    params are valid for adding a single CasbinRule entry
    """
    errors = []

    is_valid = target.ptype in constants.constants.RBAC_POLICY_TYPES
    if not is_valid:
        errors.append(build_error("policy_type", constants.INVALID_POLICY_TYPE_ERROR_MESSAGE))

    if is_valid:
        if target.ptype == "p":
            is_valid = target.v0 in constants.RBAC_ROLES
            if not is_valid:
                errors.append(build_error("role", constants.INVALID_ROLE_ERROR_MESSAGE))

            is_valid = target.v1 in constants.RBAC_RESOURCES.values()
            if not is_valid:
                errors.append(build_error("resource", constants.INVALID_RESOURCE_ERROR_MESSAGE))

            is_valid = target.v2 in constants.RBAC_ACTION_NAME_TO_METHOD_MAP.values()
            if not is_valid:
                errors.append(build_error("action", constants.INVALID_ACTION_ERROR_MESSAGE))
        else:
            try:
                v0_as_int = int(target.v0) # Don't need the value, just testing that it's an int
                is_valid = True
            except:
                is_valid = False
            if not is_valid:
                errors.append("external_admin_user_id", constants.INVALID_EXTERNAL_ADMIN_USER_ID_ERROR_MESSAGE)

            is_valid = target.v0 in constants.RBAC_ROLES
            if not is_valid:
                errors.append(build_error("role", constants.INVALID_ROLE_ERROR_MESSAGE))

    check_errors_and_return(errors)
