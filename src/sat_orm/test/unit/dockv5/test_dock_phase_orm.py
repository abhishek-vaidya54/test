import pytest

from sat_orm.dockv5 import DockPhase

@pytest.mark.input_validation
def test_dock_phase_dock_id_is_not_none():
    ''' Validates dock_phase dock_id column'''
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(dock_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_dock_phase_timestamp_is_not_none():
    ''' Validates dock_phase timestamp column'''
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(timestamp=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_dock_phase_phase_is_not_none():
    ''' Validates dock_phase phase column'''
    with pytest.raises(Exception) as exc_info:
        assert DockPhase(phase=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_dock_phase_deployment_stage_is_not_none():
    ''' Validates dock_phase deployment_stage column'''
    with pytest.raises(Exception) as exc_info:
         assert DockPhase(deployment_stage=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_return_type
def test_dock_phase_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    dock_phase = DockPhase()
    assert isinstance(dock_phase.as_dict(),dict)

@pytest.mark.test_return_type
def test_dock_phase___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    dock_phase = DockPhase()
    assert isinstance(dock_phase.__repr__(),str)