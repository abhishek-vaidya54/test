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
from sqlalchemy import ForeignKey, Column, Integer, DateTime, event
from sqlalchemy.orm import relationship

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import external_admin_user_utils, warehouse_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class UserWarehouseAssociation(Base):
    __tablename__ = "user_warehouse_association"

    external_admin_user_id = Column(
        Integer, ForeignKey("external_admin_user.id"), primary_key=True
    )
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), primary_key=True)

    external_admin_user = relationship(
        "ExternalAdminUser",
        uselist=False,
        back_populates="warehouses",
    )
    warehouse = relationship("Warehouse", uselist=False, backref="external_admin_users")

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    def as_dict(self):
        return {
            "external_admin_user_id": self.external_admin_user_id,
            "warehouse_id": self.warehouse_id,
            "external_admin_user": self.external_admin_user,
            "warehouse": self.warehouse,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(UserWarehouseAssociation, "before_insert")
def validate_role_before_insert(mapper, connection, target):
    """
    Event hook method that fires before insert
    to check if params are valid for inserting a single external_admin_user and warehouse association
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    is_valid = external_admin_user_utils.is_valid_user_id(
        connection, params_input.get("external_admin_user_id")
    )
    if not is_valid:
        errors.append(
            build_error(
                "external_admin_user_id", constants.INVALID_PARAM_USERNAME_MESSAGE
            )
        )

    is_valid = warehouse_utils.is_valid_warehouse(
        connection, params_input.get("warehouse_id"), None
    )
    if not is_valid:
        errors.append(
            build_error("warehouse_id", constants.INVALID_WAREHOUSE_ID_MESSAGE)
        )

    check_errors_and_return(errors)
