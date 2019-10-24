# Standard Library Imports

# Third Party Library Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import MessageSurvey

@pytest.mark.input_validation
def test_messages_surveys_validate_engagement():
    ''' Checks to see if engagement is Null, then returns the correct error message'''
    with pytest.raises(Exception) as exec_info:
        assert MessageSurvey(engagement=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_messages_surveys_validate_days_worn():
    ''' Checks to see if days_worn is Null, then returns the correct error message'''
    with pytest.raises(Exception) as exec_info:
        assert MessageSurvey(days_worn=None)
    assert 'cannot be Null' in str(exec_info.value)

@pytest.mark.input_validation
def test_messages_surveys_validate_modal_type():
    ''' Checks to see if modal_type is Null, then returns the correct error message'''
    with pytest.raises(Exception) as exec_info:
        assert MessageSurvey(modal_type=None)
    assert 'cannot be Null' in str(exec_info.value)
