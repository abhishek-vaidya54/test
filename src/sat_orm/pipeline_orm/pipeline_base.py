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
import os

# Third Party Library Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import casbin
from casbin_sqlalchemy_adapter import CasbinRule

connection_string = os.environ.get("PIPELINE_CONNECTION_STRING", 0)


def get_connection_string(connection_string):
    if connection_string:
        return connection_string
    else:
        raise Exception(
            "PIPELINE_CONNECTION_STRING environment variable cannot be none"
        )


engine = create_engine(get_connection_string(connection_string))
connection = engine.connect()
Session = sessionmaker(bind=connection)
session = Session()
Base = declarative_base()

# Seeding rbac policy admin role
policy_admin_exists = session.query(
    session.query(CasbinRule)
    .filter_by(v0="policy_admin", v1="rbac-roles", v2="write")
    .exists()
).scalar()

if policy_admin_exists is False:
    session.add(CasbinRule(ptype="p", v0="policy_admin", v1="rbac-roles", v2="write"))
    session.commit()
    session.close()
