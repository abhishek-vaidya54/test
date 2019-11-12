# Standard Library Imports

# Third Party Import
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import SensorEvents

@pytest.mark.input_validation
def test_sensor_events_validate_timestamp():
    ''' Validates sensor_events timestamp column'''
    with pytest.raises(Exception) as exc_info:
        assert SensorEvents(timestamp=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_sensor_events_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    sensor_events = SensorEvents()
    assert isinstance(sensor_events.as_dict(),dict)

@pytest.mark.test_return_type
def test_sensor_events___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    sensor_events = SensorEvents()
    assert isinstance(sensor_events.__repr__(),str)