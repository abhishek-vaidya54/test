'''
LICENSE:
    This file is subject to the terms and conditions defined in
    file 'LICENSE.txt', which is part of this source code package.
 
CONTRIBUTORS: 
            Vincent Turnier
CLASSIFICATION: 
            Sensitive

LINKS:
    - Please checkout the wiki for more information on SAT database ORM's:
    - https://github.com/strongarm-tech/database_models/wiki/Object-Relational-Mapper
    - https://github.com/strongarm-tech/database_models/wiki/Database-Testing

DESCRIPTION:
    The following will test the industrial athlete ORM model:
    1 - inputs
    2 - factory build
    3 - factory create
    4 - queries
    5 - relationships
'''

# Standard Library Imports

# Third Party Import
import pytest
import datetime

# Local Application Imports
# from sat_orm.pipeline import test_session
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.job_function import JobFunction
from sat_orm.pipeline_orm.shifts import Shifts
from sat_orm.pipeline_orm import industrial_athlete as ia

@pytest.mark.input_validation
def test_industrial_athlete_validate_client_id():
    ''' Validates industrial_athlete client_id column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(client_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_gender():
    ''' Validates industrial_athlete gender column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(gender=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_first_name():
    ''' Validates industrial_athlete first_name column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(first_name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_last_name():
    ''' Validates industrial_athlete last_name column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(last_name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_external_id():
    ''' Validates industrial_athlete external_id column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(external_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_warehouse_id():
    ''' Validates industrial_athlete warehouse_id column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(warehouse_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_shift_id():
    ''' Validates industrial_athlete shift_id column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(shift_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_industrial_athlete_validate_job_function_id():
    ''' Validates industrial_athlete job_function_id column'''
    with pytest.raises(Exception) as exc_info:
        assert ia.IndustrialAthlete(job_function_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_return_type
def test_industrial_athlete_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    industrial_athlete = ia.IndustrialAthlete()
    assert isinstance(industrial_athlete.as_dict(),dict)

@pytest.mark.test_return_type
def test_industrial_athlete___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    industrial_athlete = ia.IndustrialAthlete()
    assert isinstance(industrial_athlete.__repr__(),str)

@pytest.mark.relationships
def test_industrial_athlete_client_relationship(get_external_admin_user,test_session):
    ''' Test to see if relationship works correctly'''
    # TODO: connect factory boy to give an id
    client = test_session.query(Client).first()
    athlete = client.industrial_athletes[0]
    assert athlete == test_session.query(ia.IndustrialAthlete).filter_by(id=athlete.id).first()
    athlete = test_session.query(ia.IndustrialAthlete).first()
    client = athlete.client
    assert client.id != None

@pytest.mark.relationships
def test_industrial_athlete_warehouse_relationship(get_external_admin_user,test_session):
    ''' Test to see if warehouse relationship works with industrial_athlete warehouse_id foreign key'''
    # TODO: connect factory boy to give an id
    warehouse = test_session.query(Warehouse).first()
    athlete = warehouse.industrial_athletes[0]
    assert athlete == test_session.query(ia.IndustrialAthlete).filter_by(id=athlete.id).first()
    athlete = test_session.query(ia.IndustrialAthlete).first()
    warehouse = athlete.warehouse
    assert warehouse.id != None

@pytest.mark.relationships
def test_industrial_athlete_job_function_relationship(get_external_admin_user,test_session):
    ''' Test to see if job_function relationship works with industrial_athlete job_function_id foreign key'''
    # TODO: connect factory boy to give an id
    job_function = test_session.query(JobFunction).first()
    athlete = job_function.industrial_athletes[0]
    assert athlete == test_session.query(ia.IndustrialAthlete).filter_by(id=athlete.id).first()
    athlete = test_session.query(ia.IndustrialAthlete).first()
    job_function = athlete.job_function
    assert job_function.id != None

@pytest.mark.relationships
def test_industrial_athlete_shifts_relationship(get_external_admin_user,test_session):
    ''' Test to see if shifts relationship works with industrial_athlete shifts foreign key'''
    # TODO: connect factory boy to give an id
    shifts = test_session.query(Shifts).first()
    athlete = shifts.industrial_athletes[0]
    assert athlete == test_session.query(ia.IndustrialAthlete).filter_by(id=athlete.id).first()
    athlete = test_session.query(ia.IndustrialAthlete).first()
    shifts = athlete.shifts
    assert shifts.id != None



@pytest.mark.test_select
def test_get_all_athletes(get_external_admin_user,test_session):
    """
    verify we get athletes from the industrial_athlete table
    """
    result = ia.get_all_athletes(test_session)
    assert result != None




@pytest.mark.test_select
def test_dockv5_getAthletes_select_by_client_warehouse_not_terminated(get_external_admin_user,test_session):
    """
    verify all client_id and warehouse_id values from our result match what was queried for
    """
    result = ia.dockv5_getAthletes_select_by_client_warehouse_not_terminated(test_session,get_external_admin_user.client_id,get_external_admin_user.warehouses[0].warehouse_id)
    assert all([r.client_id == client_id and r.warehouse_id == warehouse_id for r in result])


@pytest.mark.test_select
def test_dockv5_getEngagement_select_by_id(get_external_admin_user,test_session):
    """
    verify the athlete_id matches what was queried for
    """
    result = ia.dockv5_getEngagement_select_by_id(test_session,get_external_admin_user.id)
    assert result.id == get_external_admin_user.id




@pytest.mark.test_select
def test_dockv5_getUpdatedAthletes_select_group_id(get_external_admin_user,test_session):
    """
    verify that athletes selected by the group_ids of the result contain the correct client_id and warehouse_id
    """
    result = ia.dockv5_getUpdatedAthletes_select_group_id(test_session,get_external_admin_user.client_id,get_external_admin_user.warehouses[0].warehouse_id)
    group_ids = [r.group_id for r in result]
    validation_result = test_session.query(ia.IndustrialAthlete).filter(ia.IndustrialAthlete.group_id in group_ids).all()
    assert all([r.client_id == client_id and r.warehouse_id == warehouse_id for r in validation_result])


@pytest.mark.test_select
def test_dockv5_getUpdatedAthletes_select_id(get_external_admin_user,test_session):
    """
    verify that athletes selected by the athlete_ids of the result contain the correct client_id and warehouse_id
    """
    result = ia.dockv5_getUpdatedAthletes_select_id(test_session,get_external_admin_user.client_id,get_external_admin_user.warehouses[0].warehouse_id)
    validation_result = test_session.query(ia.IndustrialAthlete).filter(ia.IndustrialAthlete.id in [r.id for r in result]).all()
    assert all([r.client_id == client_id and r.warehouse_id == warehouse_id for r in validation_result])



@pytest.mark.test_select
def test_dockv5_getUpdatedAthletes_select_by_db_modified(get_external_admin_user,test_session):
    """
    verify that athletes selected by the timestamp have db_modified_at >= the tiemstamp that was queried for
    """
    timestamp= '2018-01-01'
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
    result = ia.dockv5_getUpdatedAthletes_select_by_db_modified(test_session,timestamp)
    assert all([r.db_modified_at >= dt for r in result])


@pytest.mark.test_select
def test_dockv5_getUpdatedAthletes_select_by_client_warehouse_db_modified(get_external_admin_user,test_session):
    """
    verify that athletes selected by the timestamp have db_modified_at >= the tiemstamp that was queried for
    and have the correct client_id and warehouse_id
    """
    client_id,warehouse_id = 33,34
    timestamp= '2018-01-01'
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
    result = ia.dockv5_getUpdatedAthletes_select_by_client_warehouse_db_modified(test_session,client_id,warehouse_id,timestamp)
    assert all([r.db_modified_at >= dt and r.client_id == client_id and r.warehouse_id == warehouse_id for r in result])





