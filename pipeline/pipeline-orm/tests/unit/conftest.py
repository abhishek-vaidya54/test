# Standard Library
import os

# Third Party Import
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Application Import
from pipeline_orm.factories import *

def pytest_configure(config):
    ''' Adds custom test makers'''
    config.addinivalue_line('markers','input_validation: mark test to run only database validations')
    config.addinivalue_line('markers','relationships: mark tests to run only database foreign key relationships')
    config.addinivalue_line('markers','test_inserts: mark tests to run only database insert actions')
    config.addinivalue_line('markers','orm_base: mark tests to run only sqlalchemy base module test')
    config.addinivalue_line('markers','test_factories: mark tests to run only factories')

@pytest.fixture(scope='session')
def env():
    ''' Grab environment variables'''
    variables = {}
    variables['CONNECTION'] = os.environ.get('CONNECTION_STRING',0)
    if variables['CONNECTION']:
        return variables['CONNECTION']
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
    WarehouseFactory._meta.sqlalchemy_session = session
    ShiftsFactory._meta.sqlalchemy_session = session
    JobFunctionFactory._meta.sqlalchemy_session = session
    IndustrialAthleteFactory._meta.sqlalchemy_session = session
    yield session
    session.close()

@pytest.fixture(scope='function')
def industrial_athlete_factory():
    ''' Builds an IndustrialAthlete From the Factory'''
    return IndustrialAthleteFactory.build()

@pytest.fixture(scope='module', params=[2,6,5])
def client_factory(request):
    ''' Builds clients from the Factories module'''
    return ClientFactory.build_batch(size=request.param)

