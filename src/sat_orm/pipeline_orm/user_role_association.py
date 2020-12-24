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
from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship

# Local Application Import
from sat_orm.pipeline_orm.pipeline_base import Base


class UserRoleAssociation(Base):
    __tablename__ = "user_role_association"

    external_admin_user_id = Column(
        Integer, ForeignKey("external_admin_user.id"), primary_key=True
    )
    role = Column(String(30), default="manager", primary_key=True)

    external_admin_user = relationship(
        "ExternalAdminUser", uselist=False, back_populates="roles"
    )

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
            "external_admin_user": self.external_admin_user,
            "role": self.role,
        }

    def __repr__(self):
        return str(self.as_dict())
