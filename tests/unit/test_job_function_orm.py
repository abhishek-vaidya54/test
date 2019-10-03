# Third Party Imports
import pytest

# Local Application Imports
from pipeline_orm.pipeline import Warehouse
from pipeline_orm.pipeline import JobFunction

@pytest.mark.input_validation
def test_job_function_validate_warehouse_id():
    ''' Validate job_function warehouse_id Column'''
    with pytest.raises(Exception) as exc_info:
        assert JobFunction(warehouse_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_job_function_validate_name():
    ''' Validate job_function name Column'''
    with pytest.raises(Exception) as exc_info:
        assert JobFunction(name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_job_function_validate_group_administrator():
    ''' Validate job_function group_administrator Column'''
    with pytest.raises(Exception) as exc_info:
        assert JobFunction(group_administrator=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.relationships
def test_jobfunction_warehouse_relationship(session):
    ''' Test to see if warehouse relationship works with JobFunction warehouse_id foreign key'''
    # TODO: add factory boy 
    warehouse = session.query(Warehouse).filter_by(id=44).first()
    job_function = warehouse.job_functions[0]
    assert job_function == session.query(JobFunction).filter_by(id=job_function.id).first()
    job_function = session.query(JobFunction).first()
    warehouse = job_function.warehouse
    assert warehouse.id != None

