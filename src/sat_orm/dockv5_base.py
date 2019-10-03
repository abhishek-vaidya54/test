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
        raise Exception('DOCKV%_CONNECTION_STRING environment variable cannot be null')

engine = create_engine(get_connection_string(connection_string))
connection = engine.connect()
Session = sessionmaker(bind=connection)
session = Session()
Base = declarative_base()