import pytest

from sat_orm.pipeline_orm.queries import warehouse_queries


def test_get_warehouse_valid(test_session, get_warehouse_from_db):
    """
    checks if function returns correct warehouse with valid warehouse and client ids
    """
    warehouse = get_warehouse_from_db
    res = warehouse_queries.get_warehouse(test_session, warehouse.id, warehouse.client_id)
    assert res.id == warehouse.id

def test_get_warehouse_valid_none_client_id(test_session, get_warehouse_from_db):
    """
    checks if function returns correct warehouse with valid warehouse id 
    and no client id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_queries.get_warehouse(test_session, warehouse.id)
    assert res.id == warehouse.id

def test_get_warehouse_invalid_warehouse_id(test_session, get_warehouse_from_db, invalid_int):
    """
    checks if function raises exception for invalid warehouse id
    """
    warehouse = get_warehouse_from_db
    with pytest.raises(Exception):
        res = warehouse_queries.get_warehouse(test_session, invalid_int, warehouse.client_id)

def test_get_warehouse_invalid_client_id(test_session, get_warehouse_from_db, invalid_int):
    """
    checks if function raises exception for invalid client id
    """
    warehouse = get_warehouse_from_db
    with pytest.raises(Exception):
        res = warehouse_queries.get_warehouse(test_session, warehouse.id, invalid_int)

def test_get_warehouse_exists_valid(test_session, get_warehouse_from_db):
    """
    checks if function returns correct warehouse for a valid warehouse id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_queries.get_warehouse_exists(test_session, warehouse.id)
    assert res.id == warehouse.id

def test_get_warehouse_exists_invalid_warehouse_id(test_session, invalid_int):
    """
    checks if function raises exception for invalid warehouse id
    """
    with pytest.raises(Exception):
        res = warehouse_queries.get_warehouse_exists(test_session, invalid_int)