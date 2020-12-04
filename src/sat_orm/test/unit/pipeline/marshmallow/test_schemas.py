from sat_orm.pipeline import Schemas
from sat_orm.pipeline_orm.marshmallow.schemas import IndustrialAthleteSchema
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
            "db_modified_at"
        ]
    result = IndustrialAthleteSchema(only=keys).dump(ia)
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
            "db_modified_at"
        ]
    result = IndustrialAthleteSchema(only=keys).dump(ia)
    assert "id" not in result 
