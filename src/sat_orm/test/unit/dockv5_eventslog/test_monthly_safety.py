# Standard Library Imports

# Third Party Import
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import MonthlySafety

@pytest.mark.input_validation
def test_monthly_safety_validate_athlete_id():
    ''' Validates monthly_safety athlete_id column'''
    with pytest.raises(Exception) as exc_info:
        assert MonthlySafety(athlete_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_monthly_safety_validate_monthly_score():
    ''' Validates monthly_safety monthly_score column'''
    with pytest.raises(Exception) as exc_info:
        assert MonthlySafety(monthly_score=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_monthly_safety_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    monthly_safety = MonthlySafety()
    assert isinstance(monthly_safety.as_dict(),dict) 