import sat_orm.constants as constants


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
    return deployment_stage.upper() in constants.VALID_DOCK_DEPLOYMENT_STAGES


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
