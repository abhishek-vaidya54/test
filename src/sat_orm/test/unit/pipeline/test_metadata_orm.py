# Standard Library Imports

# Third Party Library Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import Metadata


@pytest.mark.input_validation
def test_metadata_validate_session_id():
    """Checks to see if session_id is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(session_id=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_metadata_validate_processed_file_id():
    """Checks to see if processed_file_id is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(processed_file_id=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_metadata_validate_metadata_type():
    """Checks to see if metadata_type is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(metadata_type=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_metadata_validate_value():
    """Checks to see if value is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(value=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_metadata_validate_exclude():
    """Checks to see if exclude is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(exclude=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_metadata_validate_db_created_at():
    """Checks to see if db_created_at is null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert Metadata(db_created_at=None)
    assert "cannot be Null" in str(exec_info.value)
