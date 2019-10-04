# Standard Library Imports

# Third Party Import
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import SurveyEvents

@pytest.mark.input_validation
def test_survey_events_validate_timestamp():
    ''' Validates survey_events timestamp column'''
    with pytest.raises(Exception) as exc_info:
        assert SurveyEvents(timestamp=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_survey_events_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    survey_events = SurveyEvents()
    assert isinstance(survey_events.as_dict(),dict)