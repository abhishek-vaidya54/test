'''
Author = Vincent Turnier
Created = September 13, 2019
Note:
    Make sure to checkout out database-models/wiki to learn more about testing
    link: https://github.com/strongarm-tech/database_models/wiki/Database-Testing

Description:
    The following test all the inputs of the config.py module. Checks to see if the
    inputes are validated. 
'''

import pytest

from dockv5_orm.config import Config, DockPhase
from dockv5_orm.config_factories import ConfigFactory, DockPhaseFactory



def test_config_dock_id_is_not_none():
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id=None,client_id=9999,warehouse_id=10234,deployment_stage='dev')
    assert "cannot be Null" in str(exc_info.value)

def test_config_client_id_is_not_none():
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id='A8E2D5D3E1A9C3',client_id=None,warehouse_id=10234,deployment_stage='dev')
    assert "cannot be Null" in str(exc_info.value)

def test_config_warehouse_id_is_not_none():
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id='A8E2D5D3E1A9C3',client_id=9999,warehouse_id=None,deployment_stage='dev')
    assert 'cannot be Null' in str(exc_info.value)

def test_config_deployment_stage_is_not_none():
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id='A8E2D5D3E1A9C3',client_id=9999,warehouse_id=10234,deployment_stage=None)
    assert 'cannot be Null' in str(exc_info.value)

def test_dock_phase_dock_id_is_not_none(dock_phase_factory):
    dock_phase = dock_phase_factory
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(dock_id=None,timestamp=dock_phase.timestamp,phase=dock_phase.phase,
                            deployment_stage=dock_phase.deployment_stage)
    assert 'cannot be Null' in str(exc_info.value)

def test_dock_phase_timestamp_is_not_none(dock_phase_factory):
    dock_phase = dock_phase_factory
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(dock_id=dock_phase.dock_id,timestamp=None,phase=dock_phase.phase,
                            deployment_stage=dock_phase.deployment_stage)
    assert 'cannot be Null' in str(exc_info.value)

def test_dock_phase_phase_is_not_none(dock_phase_factory):
    dock_phase = dock_phase_factory
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(dock_id=dock_phase.dock_id,timestamp=dock_phase.timestamp,phase=None,
                            deployment_stage=dock_phase.deployment_stage)
    assert 'cannot be Null' in str(exc_info.value)

def test_dock_phase_deployment_stage_is_not_none(dock_phase_factory):
    dock_phase = dock_phase_factory
    with pytest.raises(Exception) as exc_info:
         assert DockPhase(dock_id=dock_phase.dock_id,timestamp=dock_phase.timestamp,phase=dock_phase.phase,
                            deployment_stage=None)
    assert 'cannot be Null' in str(exc_info.value)
        

def test_config_deployment_stage_is_dev_or_prod():
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id='A8E2D5D3E1A9C3',client_id=9999,warehouse_id=10234,deployment_stage='something')
    assert str(exc_info.value) == 'deployment_stage can only be [dev,prod]'
    


