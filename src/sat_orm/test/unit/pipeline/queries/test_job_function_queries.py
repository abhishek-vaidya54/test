# def get_job_function(connection, job_function_id, warehouse_id):
from sat_orm.pipeline import JobFunction
import sat_orm.pipeline_orm.queries.job_function_queries as job_function_queries
import pytest


def test_get_job_function_valid(test_session, get_job_function_from_db):
    """
    checks if function returns correct job_function with valid job function and warehouse ids
    """
    job_function = get_job_function_from_db
    res = job_function_queries.get_job_function(
        test_session, job_function.id, job_function.warehouse_id
    )
    assert res.id == job_function.id


def test_get_job_function_invalid_warehouse_id(
    test_session, get_job_function_from_db, invalid_int
):
    """
    checks if function raises exception for invalid warehouse id
    """
    job_function = get_job_function_from_db
    with pytest.raises(Exception):
        res = job_function_queries.get_job_function(
            test_session, job_function.id, invalid_int
        )


def test_get_warehouse_invalid_jf_id(
    test_session, get_job_function_from_db, invalid_int
):
    """
    checks if function raises exception for invalid job function id
    """
    job_function = get_job_function_from_db
    with pytest.raises(Exception):
        res = job_function_queries.get_job_function(
            test_session, invalid_int, job_function.warehouse_id
        )
