'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier

CLASSIFICATION: 
            Highly Sensitive

DESCRIPTION:
            The dockv5_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.

            This file gives us the to possibility to connect our ORM
            with the proper relationships that they have.
            
            +---------------+
            | Dockv5 Tables |
            +---------------+
            | config        |
            | dock_phase    |
            +---------------+

            **** Edit This File If tables are added or removed ****
'''

# Standard Library Imports
import os

# Third Party Library Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_string = os.environ.get('DOCKV5_CONNECTION_STRING',0)

def get_connection_string(connection_string):
    if connection_string:
        return connection_string
    else:
        raise Exception('DOCKV5_CONNECTION_STRING environment variable cannot be none')

engine = create_engine(get_connection_string(connection_string))
connection = engine.connect()
Session = sessionmaker(bind=connection)
session = Session()
Base = declarative_base()