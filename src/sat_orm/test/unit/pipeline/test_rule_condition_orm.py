# Standard Libary Imports

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import RuleCondition

@pytest.mark.input_validation
def test_rule_condition_validate_path():
    '''
        Checks to see if path is Null, and if it is returns correct error 
    '''
    with pytest.raises(Exception) as exec_info:
        assert RuleCondition(path=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_condition_validate_operator():
    '''
        Checks to see if operator is Null, and if it is returns correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert RuleCondition(operator=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_condition_validate_value():
    '''
        Checks to see if value is Null, and if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert RuleCondition(value=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_condition_validate_rule_id():
    ''' 
        Checks to see if rule_id is Null, and if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert RuleCondition(rule_id=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_rule_condition_validate_deleted():
    ''' 
        Checks to see if deleted is Null, and if it is return correct error
    '''
    with pytest.raises(Exception) as exec_info:
        assert RuleCondition(deleted=None)
    assert 'cannot be Null' in str(exec_info.value)

