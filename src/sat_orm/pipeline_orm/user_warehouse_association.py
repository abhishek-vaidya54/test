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
from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants


class UserWarehouseAssociation(Base):
    __tablename__ = "user_warehouse_association"

    id = Column(Integer, primary_key=True, autoincrement=True)

    external_admin_user_id = Column(
        Integer, ForeignKey("external_admin_user.id"), primary_key=True
    )
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), primary_key=True)

    external_admin_user = relationship(
        "ExternalAdminUser", uselist=False, backref="warehouses"
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
