import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.queries import client_queries


def is_valid_client_status(status):
    """
    Helper method to check if input is a valid client status
    Return True if it is a valid client status
    Returns False if it is not valid
    """
    return status in constants.VALID_CLIENT_STATUSES


def is_valid_client_subdomain(subdomain):
    is_valid, message = utils.is_valid_string(subdomain)
    if not is_valid:
        return False, message
    return True, None


def is_valid_client_ia_name_format(field):
    return field in constants.VALID_CLIENT_IA_NAME_FORMATS


def is_valid_client_name(connection, name, id=None):
    is_valid, message = utils.is_valid_string(name)
    if not is_valid:
        return False, message

    client = client_queries.get_client_by_name(connection, name)

    if client is None:
        return True, None

    if id == client.id:
        return True, None

    return False, constants.DUPLICATE_CLIENT_NAME_MESSAGE


def is_valid_client_id(connection, id):
    """
    Helper method to check if input is a valid Client ID
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        is_valid = utils.is_valid_int(id)
        if is_valid:
            is_valid = client_queries.get_client_exists(connection, id)
        return is_valid
    except Exception as error:
        return False


def is_valid_height_unit(param_input):
    """
    Helper method to check if input is a valid height unit
    Return True if it is a valid height unit
    Returns False if it is not valid
    """
    return param_input in constants.VALID_IA_HEIGHT_UNITS


def is_valid_weight_unit(param_input):
    """
    Helper method to check if input is a valid weight unit
    Return True if it is a valid weight unit
    Returns False if it is not valid
    """
    return param_input in constants.VALID_IA_WEIGHT_UNITS