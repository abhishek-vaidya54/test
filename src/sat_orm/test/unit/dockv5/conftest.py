import os
import pytest
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from sat_orm.dockv5_factories import ConfigFactory, DockPhaseFactory

def pytest_configure(config):
    ''' Adds custom test makers'''
    config.addinivalue_line('markers','input_validation: mark test to run only database validations')
    config.addinivalue_line('markers','relationships: mark tests to run only database foreign key relationships')
    config.addinivalue_line('markers','test_inserts: mark tests to run only database insert actions')
    config.addinivalue_line('markers','orm_base: mark tests to run only sqlalchemy base module test')
    config.addinivalue_line('markers','test_factories: mark tests to run only factories')
    config.addinivalue_line('markers','test_return_type: mark tests to run only orm function return types')

@pytest.fixture(scope='session')
def env_variables():
    '''Grabbing enviromental variables '''
    env_variables = {}
    env_variables['LOCAL_DB'] = os.environ.get('DOCKV5_CONNECTION_STRING',0)
    return env_variables

@pytest.fixture(scope='module')
def engine(env_variables):
    ''' starting database engine'''
    if env_variables['LOCAL_DB']:
        engine = create_engine(env_variables['LOCAL_DB'])
        connection = engine.connect()
        yield connection
        connection.close()
    else:
        raise Exception('DOCKV5_CONNECTION_STRING Not Found. Make sure database enviroment variables are set') 

@pytest.fixture(scope='module')
def session(engine):
    ''' starting database session from database engine'''
    Session = sessionmaker(bind=engine)
    session = Session()
    ConfigFactory._meta.sqlalchemy_session = session
    DockPhaseFactory._meta.sqlalchemy_session = session
    yield session
    session.rollback()
    session.close()
    
    

@pytest.fixture(scope='function')
def config_factory():
    ''' initializes fake data for config factory without dock_phases'''
    return ConfigFactory.build(dock_phases=0)

@pytest.fixture(scope='function')
def config_factory_with_dock_phases():
    ''' initializes fake data for config factory with dock_phases'''
    return ConfigFactory.build(dock_phases=2)


@pytest.fixture(scope='function')
def dock_phase_factory():
    ''' initializes fake data for dock_phase factory'''
    return DockPhaseFactory.build()