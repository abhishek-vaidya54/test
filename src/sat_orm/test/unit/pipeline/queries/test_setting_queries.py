from sat_orm.pipeline import Setting
import sat_orm.pipeline_orm.queries.setting_queries as setting_queries
import pytest

def test_get_setting_valid(test_session, get_setting_type_athlete):
    setting = get_setting_type_athlete
    result = setting_queries.get_setting(
        connection = test_session, 
        settings_id = setting.id)
    assert setting.id == result.id

def test_get_setting_invalid(test_session):
    with pytest.raises(Exception):
        result = setting_queries.get_setting(
            connection = test_session, 
            settings_id = '')

def test_get_target_by_id_valid(test_session, get_industrial_athlete):
    ia = get_industrial_athlete
    result = setting_queries.get_target_by_id(
        connection = test_session, 
        target_type = "industrial_athlete",
        target_id = ia.id)
    assert result.id == ia.id

def test_get_target_by_id_invalid_target_id(test_session):
    with pytest.raises(Exception):
        setting_queries.get_target_by_id(
            connection = test_session, 
            target_type = "industrial_athlete",
            target_id = '')