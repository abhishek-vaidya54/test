# Standard Library Imports

# Third Party Imports
import pytest
# Local Application Imports
from sat_orm.pipeline import Rule

@pytest.mark.input_validation
def test_rule_validate_name():
    '''
        Checks to see if name is Null, if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert Rule(name=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.validation
def test_rule_validate_action():
    ''' 
        Check to see if action is Null, if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert Rule(action=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_validate_params():
    '''
        Check to see if params is Null, if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert Rule(params=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_validate_enabled():
    '''
        Check to see if enabled is Null, if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert Rule(enabled=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_validate_deleted():
    '''
        Check to see if deleted is Null, if it is return correct error 
    '''
    with pytest.raises(Exception) as exec_info:
        assert Rule(deleted=None)
    assert 'cannot be Null' in str(exec_info.value)

