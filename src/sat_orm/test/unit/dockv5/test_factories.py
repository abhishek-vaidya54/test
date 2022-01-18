import pytest
import datetime
from sat_orm.dockv5 import Config, DockPhase


def test_fake_data_type_in_ConfigFactory(config_factory):
    """Checks to see if the fake data types are correct in config factory"""
    config = config_factory
    assert len(config.dock_id) == 12
    assert isinstance(config.dock_id, str)
    assert isinstance(config.client_id, int)
    assert isinstance(config.warehouse_id, int)
    assert isinstance(config.deployment_stage, str)
    assert isinstance(config.dock_phases, list)


def test_fake_data_type_in_DockPhaseFactory(dock_phase_factory):
    """Checks to see if the fake data types are correct in dock phase factory"""
    dock_phase = dock_phase_factory
    assert isinstance(dock_phase.dock_id, Config)
    assert isinstance(dock_phase.timestamp, datetime.date)
    assert isinstance(dock_phase.phase, str)
