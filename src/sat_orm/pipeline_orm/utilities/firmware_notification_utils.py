import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import external_admin_user_utils


# def is_valid_firmware_notification(notification):
#     """
#     Helper method to check if input is a valid firmware_notification
#     Return True if it is a valid firmware_notification
#     Returns False if it is not valid
#     """
#     return notification.upper() in constants.VALID_DOCK_PHASES


def is_non_empty_string(value):
    """
    Helper method to check if input is a non empty string
    Return True if it is a non empty string
    Returns False if it is an empty string
    """
    return len(str(value.strip())) > 0


def is_valid_type(type):
    """
    Helper method to check if type is correct or not
    Return True if it is correct
    Returns False if it is not correct
    """
    if type in constants.VALID_FIRMWARE_NOTIFICATION_TYPE:
        return True
    return False


def is_valid_created_by(connection, created_by):
    """
    Helper method to check if input is a valid external admin user
    Return True if it is a valid
    Returns False if it is not valid
    """

    return external_admin_user_utils.is_valid_user_id(connection, created_by)


def is_valid_is_active(is_active):
    if is_active == True or is_active == False:
        return True
    else:
        return False
