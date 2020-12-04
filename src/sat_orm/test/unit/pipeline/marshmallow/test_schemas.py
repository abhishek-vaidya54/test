from sat_orm.pipeline_orm.marshmallow.schemas import IndustrialAthleteSchema
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete

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
