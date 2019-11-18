# Standard Library
import os

# Third Party Import
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Application Import
from sat_orm.pipeline_factories import *


def pytest_configure(config):
    ''' Adds custom test makers'''
    config.addinivalue_line(
        'markers', 'input_validation: mark test to run only database validations')
    config.addinivalue_line(
        'markers', 'relationships: mark tests to run only database foreign key relationships')
    config.addinivalue_line(
        'markers', 'test_inserts: mark tests to run only database insert actions')
    config.addinivalue_line(
        'markers', 'orm_base: mark tests to run only sqlalchemy base module test')
    config.addinivalue_line(
        'markers', 'test_factories: mark tests to run only factories')
    config.addinivalue_line(
        'markers', 'test_return_type: mark tests to run only orm function return types')
    config.addinivalue_line(
        'markers', 'test_select : mark tests to run only to verify select queries')


@pytest.fixture(scope='session')
def env():
    ''' Grab environment variables'''
    variables = {}
    variables['CONNECTION'] = os.environ.get('PIPELINE_CONNECTION_STRING', 0)
    if variables['CONNECTION']:
        return variables['CONNECTION']
    else:
        raise Exception(
            'Please make sure Environment variables are set: export CONNECTION_STRING="db://username:password@host/database"')


@pytest.fixture(scope='module')
def engine(env):
    ''' Database engine created using the environment variable fixture'''
    engine = create_engine(env)
    return engine


@pytest.fixture(scope='module')
def session(engine):
    ''' Database Session created from db connection fixture'''
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    ClientFactory._meta.sqlalchemy_session = session
    WarehouseFactory._meta.sqlalchemy_session = session
    ShiftsFactory._meta.sqlalchemy_session = session
    JobFunctionFactory._meta.sqlalchemy_session = session
    IndustrialAthleteFactory._meta.sqlalchemy_session = session
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def industrial_athlete_factory():
    ''' Builds an IndustrialAthlete From the Factory'''
    return IndustrialAthleteFactory.build()


@pytest.fixture(scope='function')
def job_function_factory():
    ''' Builds a JobFunction From the Factory'''
    return JobFunctionFactory.build()


@pytest.fixture(scope='function')
def shift_factory():
    ''' Builds a Shift From the Factory'''
    return ShiftsFactory.build()


@pytest.fixture(scope='function')
def warehouse_factory():
    ''' Builds a Warehouse From the Factory'''
    return WarehouseFactory.build()


@pytest.fixture(scope='function')
def client_factory(request):
    ''' Builds clients from the Factories module'''
    return ClientFactory.build()
