import time
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.queries import warehouse_queries
from sat_orm import constants


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


def is_valid_warehouse(connection, warehouse_id, client_id):
    """
    Validates a warehouse, checks if warehouse belongs to the client
    Returns True if it is a valid warehouse
    Returns False if it is not
    """
    try:
        warehouse = warehouse_queries.get_warehouse(connection, warehouse_id, client_id)
        return bool(warehouse)
    except Exception as error:
        return False


def is_valid_warehouse_name(connection, name, id=None):
    is_valid, message = utils.is_valid_string(name)
    if not is_valid:
        return False, message

    warehouse = warehouse_queries.get_warehouse_by_name(connection, name)

    if warehouse is None:
        return True, None

    if id == warehouse.id:
        return True, None

    return False, constants.DUPLICATE_WAREHOUSE_NAME_MESSAGE


def is_valid_week_start(value):
    """
    Helper method to check if input is a valid week_start
    Return True if it is a valid week_start
    Returns False if it is not valid
    """
    return value in constants.VALID_WEEK_START


def is_valid_utc_op_day_start(value):
    """
    Helper method to check if input is a valid utc_op_day_start
    Return True if it is a valid utc_op_day_start
    Returns False if it is not valid
    """
    try:
        time.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False
