from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.queries import external_admin_user_queries
import sat_orm.constants as constants


def is_valid_user_id(connection, id):
    """
    Helper method to check if input is a valid ExternalAdminUser ID
    Return True if it is a valid int
    Returns False if it is not valid
    """
    try:
        is_valid = utils.is_valid_int(id)
        if is_valid:
            is_valid = external_admin_user_queries.get_user_by_id(connection, id)
        return is_valid
    except Exception as error:
        return False


def is_valid_account_status(account_status):
    """
    CHECKS FOR A VALID ACCOUNT STATUS
    input - account_status
    output - True if valid or False otherwise
    """
    return account_status in constants.VALID_USER_ACCOUNT_STATUS_FORMATS
