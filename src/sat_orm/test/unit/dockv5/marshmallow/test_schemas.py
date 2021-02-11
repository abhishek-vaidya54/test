from sat_orm.dockv5 import Schemas
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete

def test_dock_phase_schema_exist(get_dock_from_db):
    """
    checks if all the mentioned fields are present in the dict
    """
    dock = get_dock_from_db
    keys = [
        "id",
        "dock_id",
        "description",
        "warehouse_id",
        "client_id",
        "dock_firmware_version",
        "timestamp",
        "phase",
        "phase_date",
        "deployment_stage",
    ]
    result = Schemas.DockPhaseSchema(only=keys).dump(dock)
    for key in keys:
        assert result[key]


def test_dock_phase_schema_does_not_exist(get_dock_from_db):
    """
    checks that no unmentioned field is present in the dict
    """
    dock = get_dock_from_db
    keys = [
        "dock_id",
        "description",
        "warehouse_id",
        "client_id",
        "dock_firmware_version",
        "timestamp",
        "phase",
        "phase_date",
        "deployment_stage",
    ]
    result = Schemas.DockPhaseSchema(only=keys).dump(dock)
    assert "id" not in result