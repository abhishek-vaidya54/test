import re
from datetime import datetime, date
from sat_orm.pipeline_orm.queries import athlete_queries
from sat_orm.pipeline_orm.queries import client_queries
from sat_orm.pipeline_orm.queries import shift_queries
from sat_orm.pipeline_orm.queries import job_function_queries
from sat_orm.pipeline_orm.queries import warehouse_queries
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils


def is_valid_string(string_input):
    """
    Helper method to check if input is a valid string
    Return [True, None] if it is a valid string
    Returns [False, reason] if it is not valid
    """
    if string_input == "":
        return False, constants.MISSING_STRING_MESSAGE
    if re.match(constants.REGEX_STRING, string_input):
        return True, None
    return False, constants.INVALID_STRING_MESSAGE


def is_valid_warehouse(session, warehouse_id):
    """
    Validates a warehouse, checks if warehouse belongs to the client
    Returns True if it is a valid warehouse
    Returns False if it is not
    """
    try:
        warehouse = warehouse_queries.get_warehouse(session, int(warehouse_id))
        return bool(warehouse)
    except Exception as error:
        return False


def is_valid_shift_timezone(timezone):
    """
    Helper method to check if input is a valid shift timezone
    Return True if it is a valid shift timezone
    Returns False if it is not valid
    """
    return timezone in constants.VALID_SHIFT_TIMEZONES


def is_valid_time(date):
    """
    Helper method to check if input is a valid datetime
    Returns True if it is a valid datetime
    Returns False if it is not a valid datetime
    """
    try:
        if date is None:
            raise ValueError()
        split_date = str(date).split(" ")
        time = (
            split_date[1].split(".")[0] if len(split_date) > 1 else date.split(".")[0]
        )
        converted_time = str(datetime.strptime(time, "%H:%M:%S").time())
        return True, converted_time
    except ValueError:
        return False, None


def is_valid_shift_id(connection, id, warehouse_id):
    """
    Helper method to check if input is a valid Shift ID
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        shift = shift_queries.get_shift(connection, id, warehouse_id)
        return bool(shift)
    except Exception as error:
        return False


def is_valid_shift_name(connection, name, id=None):
    is_valid, message = utils.is_valid_string(name)
    if not is_valid:
        return False, message

    shifts = shift_queries.get_shift_by_name(connection, name)

    if shifts is None:
        return True, None

    if id == shifts.id:
        return True, None

    return False, constants.DUPLICATE_SHIFT_NAME_MESSAGE