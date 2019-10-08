# Standard Library Imports

# Third Party Import
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import AppcrashLog

@pytest.mark.input_validation
def test_appcrash_log_validate_timestamp():
    ''' Validates appcrash_log timestamp column'''
    with pytest.raises(Exception) as exc_info:
        assert AppcrashLog(timestamp=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_appcrash_log_validate_log():
    ''' Validates appcrash_log log column'''
    with pytest.raises(Exception) as exc_info:
        assert AppcrashLog(log=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_appcrash_log_validate_dockID():
    ''' Validates appcrash_log dockID column'''
    with pytest.raises(Exception) as exc_info:
        assert AppcrashLog(dockID=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_appcrash_log_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    app_crash = AppcrashLog()
    assert isinstance(app_crash.as_dict(),dict) 

@pytest.mark.test_return_type
def test_appcrash_log_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    app_crashlogs = AppcrashLog()
    assert isinstance(app_crashlogs.as_dict(),dict)

@pytest.mark.test_return_type
def test_app_crash_log___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    app_crashlogs = AppcrashLog()
    assert isinstance(app_crashlogs.__repr__(),str)

