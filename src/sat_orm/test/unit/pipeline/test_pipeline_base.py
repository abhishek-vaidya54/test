# Standard Library Imports
import os

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline_orm import pipeline_base


@pytest.mark.orm_base
def test_get_connection_string_is_none():
    with pytest.raises(Exception) as exc_info:
        assert pipeline_base.get_connection_string(0)
    assert 'cannot be none' in str(exc_info.value)

@pytest.mark.orm_base
def test_connection_string():
    assert pipeline_base.Base
    assert pipeline_base.engine
    assert pipeline_base.connection.begin()
    assert pipeline_base.session
    assert pipeline_base.session.close() == None
    assert pipeline_base.connection.close() == None
