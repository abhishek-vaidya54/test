# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import Warehouse
from sat_orm.pipeline import JobFunction

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

@pytest.mark.test_return_type
def test_job_function_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    job_function = JobFunction()
    assert isinstance(job_function.as_dict(),dict)

@pytest.mark.test_return_type
def test_job_function___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    job_function = JobFunction()
    assert isinstance(job_function.__repr__(),str)

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

