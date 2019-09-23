import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config, DockPhase
from config_factories import ConfigFactory, DockPhaseFactory

local_conntection_string = "mysql+pymysql://root:password@localhost/dockv5"
engine = create_engine(local_conntection_string)



@pytest.fixture(scope='session')
def connection():
    connection = engine.connect()
    return connection
    # connection.close()

@pytest.fixture(scope='module')
def session(connection):
    # transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    ConfigFactory._meta.sqlalchemy_session = session
    DockPhaseFactory._meta.sqlalchemy_session = session
    return session
    # session.close()
    # transaction.rollback()


def test_insert(session):
    config_current_count = session.query(Config).count()
    dock_phase_current_count = session.query(DockPhase).count()
    config = ConfigFactory(dock_phases=1)
    config_new_count = session.query(Config).count()
    dock_phase_new_count = session.query(DockPhase).count()
    assert config_current_count != config_new_count
    assert dock_phase_current_count != dock_phase_new_count
    session.close()
    
    

