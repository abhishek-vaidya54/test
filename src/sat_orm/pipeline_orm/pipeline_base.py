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


# Third Party Library Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager

import logging

# patch(sqlalchemy=True)
LOGGER = logging.getLogger()
logging.basicConfig()


def get_connection_string(connection_string):
    if connection_string:
        return connection_string
    else:
        raise Exception(
            "PIPELINE_CONNECTION_STRING environment variable cannot be none"
        )


# engine = create_engine(get_connection_string(connection_string), pool_pre_ping=True)
# connection = engine.connect()
# session = scoped_session(sessionmaker(bind=connection))
# https://gist.github.com/brianz/2d7001bf1b0bafa9379303aa2da4cdeb


@contextmanager
def get_session():
    connection_string = os.environ.get("PIPELINE_CONNECTION_STRING", 0)

    engine = create_engine(get_connection_string(connection_string), pool_pre_ping=True)
    connection = engine.connect()
    # https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session?rq=1
    db_session = scoped_session(sessionmaker(bind=connection))

    # try:
    yield db_session

    """
        Reason for change - 
        errors in handler is been getting caught in the below except block 
        as the handler returns Exception for AWS to parse it as Bad Request.
    """
    # except Exception as error:
    #     LOGGER.exception("%s %s %s", "ERROR", "get_session()", error)
    #     return Exception(error)
    # finally:
    db_session.remove()
    connection.close()
    engine.dispose()


Base = declarative_base()
