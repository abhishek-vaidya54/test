from sat_orm.pipeline_orm.utilities import shift_utils


def test_is_valid_string_success(valid_string):
    """
    input - valid string
    output - is_valid=True, error=None
    """
    is_valid, error = shift_utils.is_valid_string(valid_string)
    assert is_valid
    assert error is None


def test_is_valid_string_failure(invalid_string):
    """
    input - valid string
    output - is_valid=False, error="Invalid string. Only a-z, A-Z, 0-9, (, ), ., - is accepted. No spaces allowed at the start or end."
    """
    is_valid, error = shift_utils.is_valid_string(invalid_string)
    assert not is_valid
    assert error is not None


def test_is_valid_warehouse_success(test_session, get_random_shift):
    """
    input - valid warehouse id
    output - is_valid=True
    """
    is_valid = shift_utils.is_valid_warehouse(
        test_session, get_random_shift.warehouse_id
    )
    assert is_valid


def test_is_valid_warehouse_failure(test_session, invalid_int):
    """
    input - invalid warehouse id
    output - is_valid=False
    """
    is_valid = shift_utils.is_valid_warehouse(test_session, invalid_int)
    assert not is_valid


def test_is_valid_shift_timezone_success(valid_timezone):
    """
    input - valid timezone
    output - is_valid=True
    """
    is_valid = shift_utils.is_valid_shift_timezone(valid_timezone)
    assert is_valid


def test_is_valid_shift_timezone_failure(invalid_string):
    """
    input - invalid timezone
    output - is_valid=False
    """
    is_valid = shift_utils.is_valid_shift_timezone(invalid_string)
    assert not is_valid


def test_is_valid_time_success(valid_datetime):
    """
    input - valid datetime
    output - is_valid=True, time_obj=converted time from datetime
    """
    is_valid, time_obj = shift_utils.is_valid_time(valid_datetime)
    assert is_valid
    assert time_obj


def test_is_valid_time_failure(invalid_string):
    """
    input - invalid datetime
    output - is_valid=False, time_obj=None
    """
    is_valid, time_obj = shift_utils.is_valid_time(invalid_string)
    assert not is_valid
    assert time_obj is None


def test_is_valid_shift_id_success(test_session, get_random_shift):
    """
    input - valid session, valid shift id, valid warehouse id
    output - is_valid=True
    """
    is_valid = shift_utils.is_valid_shift_id(
        test_session, get_random_shift.id, get_random_shift.warehouse_id
    )
    assert is_valid


def test_is_valid_shift_id_failure(test_session, invalid_int, get_random_shift):
    """
    input - valid session, invalid shift id, valid warehouse id
    output - is_valid=False
    """
    is_valid = shift_utils.is_valid_shift_id(
        test_session, invalid_int, get_random_shift.warehouse_id
    )
    assert not is_valid