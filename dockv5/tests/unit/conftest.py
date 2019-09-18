import os
import pytest
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from dockv5_orm.config_factories import ConfigFactory, DockPhaseFactory

@pytest.fixture(scope='session')
def env_variables():
    '''Grabbing enviromental variables '''
    env_variables = {}
    env_variables['LOCAL_DB'] = os.environ.get('CONNECTION_STRING',0)
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
        raise Exception('Database Connection String Not Found. Make sure database enviroment variables are set') 

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