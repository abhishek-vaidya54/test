# Standard Library Imports

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import ProcessedFile


@pytest.mark.input_validation
def test_processed_file_validate_name():
    """Checks to see if name is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(name=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_status():
    """Checks to see if status is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(status=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_version():
    """Checks to see if status is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(version=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_lateral_angle_exceeded_limit():
    """Checks to see if lateral_angle_exceeded_limit is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(lateral_angle_exceeded_limit=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_lateral_vel_exceeded_limit():
    """Check to see if lateral_vel_exceeded_limit is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(lateral_vel_exceeded_limit=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_twist_vel_exceeded_limit():
    """Checks to see if twist_vel_exceeded_limit is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(twist_vel_exceeded_limit=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_cropping_time():
    """Checks to see if cropping_time is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(cropping_time=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_cropping_percentage():
    """Checks to see if cropping_percentage is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(cropping_percentage=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_work_time():
    """Checks to see if work_time is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(work_time=None)
    assert "cannot be Null" in str(exec_info.value)


@pytest.mark.input_validation
def test_processed_file_validate_sg_position_limit():
    """Checks to see if sg_position_limit is Null and returns the correct error message"""
    with pytest.raises(Exception) as exec_info:
        assert ProcessedFile(sg_position_limit=None)
    assert "cannot be Null" in str(exec_info.value)
