# Standard Library Imports
import os

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.dockv5_eventslog import EngagementStats

@pytest.mark.input_validation
def test_engagement_stats_validate_athlete_id():
    ''' Validates appcrash_log athlete_id column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(athlete_id=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_engagement_stats_validate_days_worn_haptic_enable():
    ''' Validates appcrash_log days_worn_haptic_enable column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(days_worn_haptic_enable=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_engagement_stats_validate_days_worn_haptic_disable():
    ''' Validates appcrash_log days_worn_haptic_disable column'''
    with pytest.raises(Exception) as exc_info:
        assert EngagementStats(days_worn_haptic_disable=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_as_dict
def test_engagement_stats_as_dict():
    ''' Checks to see if as_dict returns a dictionary'''
    engagement_stats = EngagementStats()
    assert isinstance(engagement_stats.as_dict(),dict) 