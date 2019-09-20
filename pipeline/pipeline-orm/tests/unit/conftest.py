# Standard Library
import os

# Third Party Import
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Application Import
from pipeline_orm.factories import IndustrialAthleteFactory, ClientFactory

def pytest_configure(config):
    ''' Adds custom test makers'''
    config.addinivalue_line('markers','input_validation: mark test to run only database validations')
    config.addinivalue_line('markers','relationships: mark tests ro run only database foreign key relationships')
    config.addinivalue_line('markers','insert_test: mark tests ro run only database insert actions')

@pytest.fixture(scope='session')
def env():
    ''' Grab environment variables'''
    variables = {}
    variables['LOCAL_DB'] = os.environ.get('CONNECTION_STRING',0)
    if variables['LOCAL_DB']:
        return variables['LOCAL_DB']
    else:
        raise Exception('Please make sure Environment variables are set: export CONNECTION_STRING="db://username:password@host/database"')

@pytest.fixture(scope='module')
def connection(env):
    ''' Database engine created using the environment variable fixture'''
    engine = create_engine(env)
    connection = engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope='module')
def session(connection):
    ''' Database Session created from db connection fixture'''
    Session = sessionmaker(bind=connection)
    session = Session()
    ClientFactory._meta.sqlalchemy_session = session
    IndustrialAthleteFactory._meta.sqlalchemy_session = session
    yield session
    session.close()

@pytest.fixture(scope='function')
def industrial_athlete_factory():
    ''' Builds an IndustrialAthlete From the Factory'''
    return IndustrialAthleteFactory.build()