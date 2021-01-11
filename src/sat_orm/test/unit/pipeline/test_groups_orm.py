# Third Party Import
import pytest

# Local Application Imports
from sat_orm.pipeline import Groups, IndustrialAthlete

@pytest.mark.test_return_type
def test_groups_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    group = Groups()
    assert isinstance(group.as_dict(),dict)

@pytest.mark.test_return_type
def test_groups___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    group = Groups()
    assert isinstance(group.__repr__(),str)


@pytest.mark.relationships
def test_groups_industrial_athlete_relationship(test_session, get_group_from_db, get_external_admin_user):
    """ Test to see if relationship works correctly """
    ia = test_session.query(IndustrialAthlete).first()
    group = get_group_from_db
    ia.group_id = group.id
    assert group == ia.groups

