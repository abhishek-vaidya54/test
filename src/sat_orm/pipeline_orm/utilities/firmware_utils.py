import re
import sat_orm.constants as constants
from sat_orm.pipeline_orm.queries import firmware_queries
from sat_orm.pipeline_orm.utilities import utils


def is_non_empty_string(value):
    """
    Helper method to check if input is a non empty string
    Return True if it is a non empty string
    Returns False if it is an empty string
    """
    return len(str(value.strip())) > 0


def is_valid_device_type_id(connection, device_type_id):
    """
    Helper method to check if input is a valid device type
    Return True if it is a valid
    Returns False if it is not valid
    """
    try:
        is_valid = utils.is_valid_int(device_type_id)
        if is_valid:
            is_valid = firmware_queries.get_device_type_by_id(
                connection, device_type_id
            )
        return is_valid
    except Exception as error:
        return False


def is_valid_hardware_id(connection, hardware_id):
    """
    Helper method to check if input is a valid hardware
    Return True if it is a valid
    Returns False if it is not valid
    """
    try:
        is_valid = utils.is_valid_int(hardware_id)
        if is_valid:
            is_valid = firmware_queries.get_hardware_by_id(connection, hardware_id)
        return is_valid
    except Exception as error:
        return False


def is_valid_url(url):
    """
    Helper method to check if input is a valid url
    Return True if it is a valid
    Returns False if it is not valid
    """
    try:
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        is_valid = re.match(regex, url) is not None
        return is_valid
    except Exception as error:
        return False
