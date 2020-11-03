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

from ddtrace import patch

patch(sqlalchemy=True)

# Third Party Library Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager

import logging

LOGGER = logging.getLogger()
logging.basicConfig()


def get_connection_string(connection_string):
    if connection_string:
        return connection_string
    else:
        raise Exception("DOCKV5_CONNECTION_STRING environment variable cannot be none")


@contextmanager
def get_session():
    connection_string = os.environ.get("DOCKV5_CONNECTION_STRING", 0)

    engine = create_engine(get_connection_string(connection_string), pool_pre_ping=True)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(bind=connection))

    yield db_session
    db_session.remove()
    connection.close()


Base = declarative_base()
