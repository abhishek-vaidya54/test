from sat_orm.pipeline import Schemas
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete


def test_external_admin_user_serializer(
    get_external_admin_user, valid_external_admin_user_fields
):
    """
    input - valid external admin user fields, valid external admin user
    output - valid external admin user dict
    """
    user_dict = Schemas.ExternalAdminUserSchema(
        only=valid_external_admin_user_fields
    ).dump(get_external_admin_user)
    assert len(user_dict.keys()) == len(valid_external_admin_user_fields)
    for field in valid_external_admin_user_fields:
        assert field in user_dict


def test_shift_serializer(get_random_shift, valid_shift_fields):
    """
    input - valid shift fields, valid shift
    output - valid shift dict
    """
    shift_dict = Schemas.ShiftsSchema(only=valid_shift_fields).dump(get_random_shift)
    assert len(shift_dict.keys()) == len(valid_shift_fields)
    for field in valid_shift_fields:
        assert field in shift_dict


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
    result = Schemas.SettingSchema(only=keys).dump(setting)
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
    result = Schemas.SettingSchema(only=keys).dump(setting)
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
    result = Schemas.WarehouseSchema(only=keys).dump(warehouse)
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
    result = Schemas.WarehouseSchema(only=keys).dump(warehouse)
    assert "id" not in result


def test_ia_schema_valid(get_external_admin_user, test_session):
    """
    checks marshmallow schema with correct keys
    """
    ia = test_session.query(IndustrialAthlete).first()
    keys = [
        "id",
        "firstName",
        "lastName",
        "externalId",
        "sex",
        "shiftId",
        "jobFunctionId",
        "warehouseId",
        "hireDate",
        "terminationDate",
        "db_created_at",
        "db_modified_at",
    ]
    result = Schemas.IndustrialAthleteSchema(only=keys).dump(ia)
    for key in keys:
        assert key in result


def test_ia_schema_invalid(get_external_admin_user, test_session):
    """
    checks marshmallow schema with missing id key
    """
    ia = test_session.query(IndustrialAthlete).first()
    keys = [
        "firstName",
        "lastName",
        "externalId",
        "sex",
        "shiftId",
        "jobFunctionId",
        "warehouseId",
        "hireDate",
        "terminationDate",
        "db_created_at",
        "db_modified_at",
    ]
    result = Schemas.IndustrialAthleteSchema(only=keys).dump(ia)
    assert "id" not in result


def test_client_schema_valid(client_factory, test_session):
    """
    checks marshmallow schema with correct keys
    Input: client table first row and client table selected columns
    """
    keys = [
        "id",
        "name",
        "status",
        "contracted_users",
        "active_inactive_date",
        "ia_name_format",
        "db_created_at",
        "db_modified_at",
    ]
    result = Schemas.ClientSchema(only=keys).dump(client_factory)
    for key in keys:
        assert result[key]


def test_client_schema_invalid(client_factory, test_session):
    """
    checks marshmallow schema with missing id key
    Input: client table first row and client table selected columns except id
    Output: True if id not in result
    """
    keys = [
        "name",
        "status",
        "contracted_users",
        "active_inactive_date",
        "ia_name_format",
        "db_created_at",
        "db_modified_at",
    ]
    result = Schemas.ClientSchema(only=keys).dump(client_factory)
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
    result = Schemas.JobFunctionSchema(only=keys).dump(job_function)
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
    result = Schemas.JobFunctionSchema(only=keys).dump(job_function)
    assert "id" not in result
