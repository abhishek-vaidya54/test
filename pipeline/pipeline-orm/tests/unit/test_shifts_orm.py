# Third Party Imports
import pytest

# Local Application Import
from pipeline_orm.pipeline import Warehouse
from pipeline_orm.pipeline import Shifts

@pytest.mark.input_validation
def test_shifts_validate_warehouse_id():
    ''' Validate shifts warehouse_id Column'''
    with pytest.raises(Exception) as exc_info:
        assert Shifts(warehouse_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_shifts_validate_name():
    ''' Validate shifts name Column'''
    with pytest.raises(Exception) as exc_info:
        assert Shifts(name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_shifts_validate_shift_start():
    ''' Validate shifts shift_start Column'''
    with pytest.raises(Exception) as exc_info:
        assert Shifts(shift_start=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_shifts_validate_shift_end():
    ''' Validate shifts shift_end Column'''
    with pytest.raises(Exception) as exc_info:
        assert Shifts(shift_end=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_shifts_validate_group_administrator():
    ''' Validate shifts group_administrator Column'''
    with pytest.raises(Exception) as exc_info:
        assert Shifts(group_administrator=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.relationships
def test_shifts_warehouse_relationship(session):
    ''' Test to see if warehouse relationship works with JobFunction warehouse_id foreign key'''
    # TODO: add factory boy 
    warehouse = session.query(Warehouse).filter_by(id=44).first()
    shifts = warehouse.shifts[0]
    assert shifts == session.query(Shifts).filter_by(id=shifts.id).first()