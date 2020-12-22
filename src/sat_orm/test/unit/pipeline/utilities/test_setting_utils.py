import sat_orm.constants as constants
from sat_orm.pipeline import Setting, IndustrialAthlete
import sat_orm.pipeline_orm.utilities.setting_utils as setting_utils

import pytest
import random


# is_valid_target_type,
# is_valid_target_id,
# is_valid_value_obj

def test_is_valid_target_type_valid():
    assert setting_utils.is_valid_target_type(random.choice(constants.VALID_TARGET_TYPES))

def test_is_valid_target_type_invalid():
    assert setting_utils.is_valid_target_type(" ") is False
    
def test_is_valid_target_id_valid(test_session, get_industrial_athlete):
    ia = get_industrial_athlete
    result, message = setting_utils.is_valid_target_id(
        connection = test_session, 
        target_type = "industrial_athlete",
        target_id = ia.id)
    assert result

def test_is_valid_target_id_invalid_target_id(test_session):
    result, message = setting_utils.is_valid_target_id(
        connection = test_session, 
        target_type = "industrial_athlete",
        target_id = '')
    assert result is False

def test_is_valid_value_obj_valid():
    result, message = setting_utils.is_valid_value_obj

def test_is_valid_value_obj_valid(settings_factory):
    result, message = setting_utils.is_valid_value_obj(settings_factory.value)
    assert result