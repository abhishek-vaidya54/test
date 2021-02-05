from email.utils import parseaddr
import sat_orm.constants as constants


def is_valid_group_admin(value):
    result = parseaddr(value)
    return result[1]


def is_valid_package_unit(param_input):
    """
    Helper method to check if input is a valid package unit
    Return True if it is a valid package unit
    Returns False if it is not valid
    """
    return param_input in constants.VALID_PACKAGE_UNITS
