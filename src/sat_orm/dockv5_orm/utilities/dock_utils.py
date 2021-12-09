import sat_orm.constants as constants
import utilities.validations.ia_validator as ia_validator
from sat_orm.dockv5_orm.queries import dock_queries
from utilities.error_handler.error_handler import return_error_response
from sat_orm.pipeline_orm.utilities import utils


def is_valid_dock_phase(phase):
    """
    Helper method to check if input is a valid dock phase
    Return True if it is a valid dock phase
    Returns False if it is not valid
    """
    return phase.upper() in constants.VALID_DOCK_PHASES


def is_valid_dock_deployment_stage(deployment_stage):
    """
    Helper method to check if input is a valid dock deployment stage
    Return True if it is a valid dock deployment stage
    Returns False if it is not valid
    """
    if deployment_stage.upper() in constants.VALID_DOCK_DEPLOYMENT_STAGES:
        return True, None
    else:
        return False, constants.INVALID_DEPLOYMENT_STAGE_MESSAGE


def is_valid_dock_firmware_version(firmware_version):
    """
    Helper method to check if input is a valid dock firmware version
    Return True if it is a valid dock firmware version
    Returns False if it is not valid
    """
    return len(str(firmware_version).split(".")) > 1


def is_non_empty_string(value):
    """
    Helper method to check if input is a non empty string
    Return True if it is a non empty string
    Returns False if it is an empty string
    """
    return len(str(value.strip())) > 0


def is_valid_dock_id(session, dock_id):
    """
    Helper method to check if input is a valid DockPhase ID
    Return True if it is a valid int
    Returns False if it is not valid
    """
    dock_id_length = 12
    if len(dock_id) != dock_id_length:
        return False, constants.INVALID_DOCK_ID_LENGTH_MESSAGE
    dock = dock_queries.get_dock_exists(session, dock_id)
    if dock is None:
        return True, None
    return False, constants.DUPLICATE_DOCK_ID_MESSAGE
