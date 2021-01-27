import pytest
from sat_orm.pipeline_orm.queries import athlete_queries
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete

def test_get_ia_by_external_id_valid(get_external_admin_user, test_session):
    """
        Checks if get_ia_by_external_id method is returning ia row
        Input:
            external id, warehouse_id
        Output:
            ia row
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = athlete_queries.get_ia_by_external_id(test_session, ia.external_id , ia.warehouse_id)
    assert result

def test_get_ia_by_external_id_invalid(get_external_admin_user,invalid_id, test_session):
    """
        Checks if get_ia_by_external_id method is returning False or not
        Input:
            invalid_id, warehouse_id
        Output:
            None
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = athlete_queries.get_ia_by_external_id(test_session, invalid_id , ia.warehouse_id)
    assert result == None