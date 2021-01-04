from sat_orm.pipeline_orm.marshmallow.schemas import *

def test_setting_schema_exist(get_setting_type_athlete):
    """
    checks if all the mentioned fields are present in the dict
    """
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
    """
    checks that no unmentioned field is present in the dict
    """
    setting = get_setting_type_athlete
    keys = [
            "target_type",
            "target_id",
        ]
    result = SettingSchema(only=keys).dump(setting)
    assert "id" not in result

def test_warehouse_schema_exist(get_warehouse_from_db):
    """
    checks if all the mentioned fields are present in the dict
    """
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
    """
    checks that no unmentioned field is present in the dict
    """
    warehouse = get_warehouse_from_db
    keys = [
            "client_id",
            "name",
            "location",
        ]
    result = WarehouseSchema(only=keys).dump(warehouse)
    assert "id" not in result

def test_job_function_schema_exist(get_job_function_from_db):
    """
    checks if all the mentioned fields are present in the dict
    """
    job_function = get_job_function_from_db
    keys = [
            "id",
            "warehouse_id",
            "name",
            "max_package_mass",
        ]
    result = JobFunctionSchema(only=keys).dump(job_function)
    for key in keys:
        assert result[key]

def test_job_function_schema_does_not_exist(get_job_function_from_db):
    """
    checks that no unmentioned field is present in the dict
    """
    job_function = get_job_function_from_db
    keys = [
            "warehouse_id",
            "name",
            "max_package_mass",
        ]
    result = JobFunctionSchema(only=keys).dump(job_function)
    assert "id" not in result

