# Standard Library Imports
import os

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import EngagementStats

@pytest.mark.input_validation
def test_engagement_stats_validate_athlete_id():
    ''' Validates engagement_stats athlete_id column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(athlete_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_engagement_stats_validate_days_worn_haptic_enable():
    ''' Validates engagement_stats days_worn_haptic_enable column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(days_worn_haptic_enable=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_engagement_stats_validate_days_worn_haptic_disable():
    ''' Validates engagement_stats days_worn_haptic_disable column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(days_worn_haptic_disable=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_engagement_stats_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    engagement_stats = EngagementStats()
    assert isinstance(engagement_stats.as_dict(),dict) 

@pytest.mark.test_return_type
def test_engagement_stats___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    engagement_stats = EngagementStats()
    assert isinstance(engagement_stats.__repr__(),str)