from sat_orm.dockv5_orm.utilities import dock_utils
import sat_orm.constants as constants
import random
from sat_orm.dockv5 import DockPhase
import uuid


def test_is_valid_dock_phase():
    """
    Test method to check is_valid_dock_phase method
    """
    valid_phase = random.choice(constants.VALID_DOCK_PHASES)
    assert dock_utils.is_valid_dock_phase(valid_phase)


def test_is_valid_dock_deployment_stage():
    """
    Test method to check is_valid_dock_deployment_stage method
    """
    valid_dep_stage = random.choice(constants.VALID_DOCK_DEPLOYMENT_STAGES)
    assert dock_utils.is_valid_dock_deployment_stage(valid_dep_stage)


def test_is_valid_dock_firmware_version(test_dock_session):
    """
    Test method to check is_valid_dock_firmware_version method
    """
    firmware_version = test_dock_session.query(DockPhase).first().dock_firmware_version
    assert dock_utils.is_valid_dock_firmware_version(firmware_version)


def test_is_non_empty_string():
    """
    Test method to check is_non_empty_string method
    """
    valid_string = str(uuid.uuid4())
    assert dock_utils.is_non_empty_string(valid_string)
