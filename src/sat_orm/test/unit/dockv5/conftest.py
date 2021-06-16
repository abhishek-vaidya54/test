import os
import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sat_orm.dockv5_factories import DockPhaseFactory, ConfigFactory
from sat_orm.test.test_database.test_database_setup import create_test_db
from sat_orm.test.unit.pipeline.conftest import test_session, get_external_admin_user

from sat_orm.dockv5 import (
    DockPhase,
    get_session as get_dock_session,
    # connection as dockConnection,
)


@pytest.fixture(scope="session")
def test_dock_session():
    """ Database Session created from db connection fixture"""
    is_created, error = create_test_db("dock")
    if is_created:
        os.environ[
            "DOCKV5_CONNECTION_STRING"
        ] = "mysql+pymysql://root:password@127.0.01:3306/test_dock"
        """ Database Session created from db connection fixture"""
        with get_dock_session() as dockSession:
            # transaction = dockConnection.begin()
            DockPhaseFactory._meta.sqlalchemy_session = dockSession
            ConfigFactory._meta.sqlalchemy_session = dockSession
            dockv5 = dockSession.query(func.max(DockPhase.id)).first()
            dock_max_id = 1
            if dockv5[0] is not None:
                dock_max_id = dockv5[0] + 1
            DockPhaseFactory.reset_sequence(dock_max_id)
            ConfigFactory.reset_sequence(dock_max_id)

            yield dockSession
    else:
        RuntimeError(error)


@pytest.fixture(scope="function")
def get_dock_from_db(test_session, test_dock_session, get_external_admin_user):
    user = get_external_admin_user
    """ Creates dock from the Factories module"""
    dock = DockPhaseFactory(client_id=user.client_id, warehouse_id=user.warehouse_id)
    config = ConfigFactory(dock_id=dock.dock_id, client_id=user.client_id, warehouse_id=user.warehouse_id)

    return dock