from email.utils import parseaddr
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.queries import job_function_queries


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


def is_valid_job_function_name(connection, name, id=None, warehouse_id=None):
    is_valid, message = utils.is_valid_string(name)
    if not is_valid:
        return False, message

    job_function = job_function_queries.get_job_function_by_name(connection, name, warehouse_id)

    if job_function is None:
        return True, None

    if id == job_function.id:
        return True, None

    return False, constants.DUPLICATE_JOB_FUNCTION_NAME_MESSAGE
