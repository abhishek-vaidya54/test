import copy
from email.utils import parseaddr
import re
from datetime import datetime, date


import sat_orm.constants as constants


def build_error(field_name, reason):
    error = copy.deepcopy(constants.ERROR_DATA)
    error["fieldName"] = field_name
    error["reason"] = reason
    return error


def is_valid_date(date_input):
    """
    Helper method to check if input is a valid date (MM/dd/YY)
    Returns True if it is a valid date
    Returns False if it is not a valid date
    """
    try:
        if isinstance(date_input, datetime) or isinstance(date_input, date):
            return True, date_input
        if date_input is None:
            raise ValueError()
        date_str = str(datetime.strptime(date_input, "%m/%d/%Y").date())
        return True, date_str
    except ValueError:
        return False, None


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


def is_valid_int(int_input):
    """
    Helper method to check if input is a valid integer
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        int(int_input)
        return True, None
    except ValueError:
        return False, constants.INVALID_INTEGER_MESSAGE


def is_valid_float(float_input):
    """
    Helper method to check if input is a valid float
    Return True if it is a valid float
    Returns False if it is not valid
    """
    try:
        float(float_input)
        return True, None
    except ValueError:
        return False, constants.INVALID_FLOAT_MESSAGE


def is_valid_bool(bool_input):
    """
    Helper method to check if input is a valid boolean
    Return True if it is a valid bool
    Returns False if it is not valid
    """
    is_valid = isinstance(bool_input, bool)
    if is_valid:
        return True, None

    return False, constants.INVALID_BOOLEAN_MESSAGE

def is_valid_email(email):
    """
    CHECKS FOR A VALID EMAIL
    input - email
    output - True if valid or False otherwise
    """
    return bool(re.match(constants.EMAIL_REGEX, email))