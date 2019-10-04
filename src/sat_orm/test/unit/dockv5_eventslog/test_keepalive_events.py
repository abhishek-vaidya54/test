# Standard Library Imports

# Third Party Import
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import KeepaliveEvents

@pytest.mark.input_validation
def test_keepalive_events_validate_timestamp():
    ''' Validates keepalive_events timestamp column'''
    with pytest.raises(Exception) as exc_info:
        assert KeepaliveEvents(timestamp=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_keepalive_events_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    keepalive_events = KeepaliveEvents()
    assert isinstance(keepalive_events.as_dict(),dict) 
