from sat_orm.pipeline_orm.marshmallow.schemas import *

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

def test_warehouse_schema_exist(get_warehouse_from_db):
    warehouse = get_warehouse_from_db
    keys = [
            "id",
            "client_id",
            "name",
            "location",
        ]
    result = WarehouseSchema(only=keys).dump(warehouse)
    for key in keys:
        assert result[key]

def test_warehouse_schema_does_not_exist(get_warehouse_from_db):
    warehouse = get_warehouse_from_db
    keys = [
            "client_id",
            "name",
            "location",
        ]
    result = WarehouseSchema(only=keys).dump(warehouse)
    assert "id" not in result

