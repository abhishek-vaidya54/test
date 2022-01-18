# Standard Library Imports

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import ParserMonitor


@pytest.mark.input_validation
def test_parser_monitor_session_id():
    """
    Checks to see if session_id is Null, if it is return correct error
    """
    with pytest.raises(Exception) as exec_info:
        assert ParserMonitor(session_id=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_parser_monitor_file_status():
    """
    Checks to see if file_status is Null, if it is return correct error
    """
    with pytest.raises(Exception) as exec_info:
        assert ParserMonitor(file_status=None)
    assert "cannot be Null" in str(exec_info.value)
