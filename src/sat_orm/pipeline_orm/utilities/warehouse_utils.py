from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.queries import warehouse_queries

def is_valid_lat_long(key, value):
    """
    Helper method that checks if input is valid latitude or longitude
    """
    try:
        parsed = float(value)
        if key == "latitude":
            return parsed >= -90 and parsed <= 90
        else:
            return parsed >= -180 and parsed <= 180
    except:
        return False

def is_valid_lat_long_direction(value):
    return value in ("N", "S", "E", "W")

def is_valid_warehouse_id(connection, id):
    """
    Helper method to check if input is a valid Warehouse ID
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        is_valid = utils.is_valid_int(id)
        if is_valid:
            is_valid = warehouse_queries.get_warehouse_exists(connection, id)
        return is_valid
    except:
        return False