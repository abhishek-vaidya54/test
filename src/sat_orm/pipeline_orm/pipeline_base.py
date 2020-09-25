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
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_string = os.environ.get("PIPELINE_CONNECTION_STRING", 0)


def strong_reference_session(session):
    @event.listens_for(session, "pending_to_persistent")
    @event.listens_for(session, "deleted_to_persistent")
    @event.listens_for(session, "detached_to_persistent")
    @event.listens_for(session, "loaded_as_persistent")
    def strong_ref_object(sess, instance):
        if "refs" not in sess.info:
            sess.info["refs"] = refs = set()
        else:
            refs = sess.info["refs"]

        refs.add(instance)

    @event.listens_for(session, "persistent_to_detached")
    @event.listens_for(session, "persistent_to_deleted")
    @event.listens_for(session, "persistent_to_transient")
    def deref_object(sess, instance):
        sess.info["refs"].discard(instance)


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
strong_reference_session(session)
Base = declarative_base()
