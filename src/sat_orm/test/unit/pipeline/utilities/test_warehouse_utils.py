import random

from sat_orm.pipeline_orm.utilities import warehouse_utils

# def is_valid_lat_long(key, value):

# def is_valid_lat_long_direction(value):

# def is_valid_warehouse_id(connection, id):

# def is_valid_warehouse(connection, warehouse_id, client_id):
   
def test_is_valid_lat_long_valid():
    """
    checks if function returns true for correct params 
    """
    latitude = warehouse_utils.is_valid_lat_long("latitude", 85)
    longitude = warehouse_utils.is_valid_lat_long("longitude", 85)
    assert latitude
    assert longitude

def test_is_valid_lat_long_invalid():
    """
    checks if function returns false for incorrect params 
    """
    latitude = warehouse_utils.is_valid_lat_long("latitude", 200)
    longitude = warehouse_utils.is_valid_lat_long("longitude", 200)
    assert latitude is False
    assert longitude is False

def test_is_valid_lat_long_direction_valid():
    """
    checks if function returns true for correct params 
    """
    res = warehouse_utils.is_valid_lat_long_direction(random.choice(["N", "S", "E", "W"]))
    assert res

def test_is_valid_lat_long_direction_invalid():
    """
    checks if function returns false for incorrect params 
    """
    res = warehouse_utils.is_valid_lat_long_direction("A")
    assert res is False

def test_is_valid_warehouse_id_valid(test_session, get_warehouse_from_db):
    """
    checks if function returns true for valid warehouse id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_utils.is_valid_warehouse_id(test_session, warehouse.id)
    assert res

def test_is_valid_warehouse_id_invalid(test_session, invalid_int):
    """
    checks if function returns false for invalid warehouse id
    """
    res = warehouse_utils.is_valid_warehouse_id(test_session, invalid_int)
    assert res is False

def test_is_valid_warehouse_valid(test_session, get_warehouse_from_db):
    """
    checks if function returns true for valid warehouse id and client_id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_utils.is_valid_warehouse(test_session, warehouse.id, warehouse.client_id)
    assert res

def test_is_valid_warehouse_invalid_warehouse_id(test_session, invalid_int, get_warehouse_from_db):
    """
    checks if function returns false for invalid warehouse id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_utils.is_valid_warehouse(test_session, invalid_int, warehouse.client_id)
    assert res is False

def test_is_valid_warehouse_invalid_client_id(test_session, invalid_int, get_warehouse_from_db):
    """
    checks if function returns false for invalid client id
    """
    warehouse = get_warehouse_from_db
    res = warehouse_utils.is_valid_warehouse(test_session, warehouse.id, invalid_int)
    assert res is False
