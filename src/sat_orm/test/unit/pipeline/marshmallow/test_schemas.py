from sat_orm.pipeline_orm.marshmallow.schemas import SettingSchema

def test_setting_schema_exist(get_setting_type_athlete):
    setting = get_setting_type_athlete
    keys = [
            "id",
            "target_type",
            "target_id",
        ]
    result = SettingSchema(only=keys).dump(setting)
    for key in keys:
        assert result[key]

def test_setting_schema_does_not_exist(get_setting_type_athlete):
    setting = get_setting_type_athlete
    keys = [
            "target_type",
            "target_id",
        ]
    result = SettingSchema(only=keys).dump(setting)
    assert "id" not in result