from sat_orm.pipeline_orm.queries import shift_queries
import pytest


def test_get_shift_success(test_session, get_random_shift):
    """
    input - valid shift id, valid warehouse id
    output - valid shift
    """
    shift = shift_queries.get_shift(
        test_session, get_random_shift.id, get_random_shift.warehouse_id
    )
    assert shift.id == get_random_shift.id
    assert shift.warehouse_id == get_random_shift.warehouse_id


def test_get_shift_failure(test_session, invalid_int, get_random_shift):
    """
    input - invalid shift id, valid warehouse id
    output - Error
    """
    with pytest.raises(Exception):
        shift = shift_queries.get_shift(
            test_session, invalid_int, get_random_shift.warehouse_id
        )
