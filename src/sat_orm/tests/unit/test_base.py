# Standard Library Imports
import os

# Third Party Imports
import pytest

# Local Application Imports
from pipeline_orm import base


@pytest.mark.orm_base
def test_get_connection_string_is_none():
    with pytest.raises(Exception) as exc_info:
        assert base.get_connection_string(0)
    assert 'cannot be none' in str(exc_info.value)

@pytest.mark.orm_base
def test_connection_string():
    assert base.Base
    assert base.engine
    assert base.connection.begin()
    assert base.session
    assert base.session.close() == None
    assert base.connection.close() == None
