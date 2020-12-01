from sat_orm.pipeline_orm.marshmallow.schemas import ClientSchema
from sat_orm.pipeline import Client

def test_client_schema_valid(test_session):
    """
        checks marshmallow schema with correct keys
        Input: client table first row and client table selected columns
    """
    client = test_session.query(Client).first()
    keys = [
            "id",
            "name",
            "status",
            "contracted_users",
            "active_inactive_date",
            "ia_name_format",
            "db_created_at",
            "db_modified_at"
        ]
    result = ClientSchema(only=keys).dump(client)
    for key in keys:
        assert result[key]

def test_client_schema_invalid(test_session):
    """
        checks marshmallow schema with missing id key
        Input: client table first row and client table selected columns except id
        Output: True if id not in result
    """
    client = test_session.query(Client).first()
    keys = [
            "name",
            "status",
            "contracted_users",
            "active_inactive_date",
            "ia_name_format",
            "db_created_at",
            "db_modified_at"
        ]
    result = ClientSchema(only=keys).dump(client)
    assert "id" not in result