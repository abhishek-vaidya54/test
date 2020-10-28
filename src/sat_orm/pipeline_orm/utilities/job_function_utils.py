import re
from datetime import datetime, date
from sat_orm.pipeline_orm.queries import job_function_queries
import sat_orm.constants as constants
from email.utils import parseaddr

def is_valid_float(float_input):
    """
    Helper method to check if input is a valid integer
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        float(float_input)
        return True, None
    except ValueError:
        return False, constants.INVALID_FLOAT_MESSAGE


def is_valid_group_admin(value):
    result = parseaddr(value)
    return result[1]
