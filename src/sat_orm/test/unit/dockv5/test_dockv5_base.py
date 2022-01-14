# Standard Library Imports
import os

# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.dockv5_orm import dockv5_base


@pytest.mark.orm_base
def test_get_connection_string_is_none():
    with pytest.raises(Exception) as exc_info:
        assert dockv5_base.get_connection_string(0)
    assert "cannot be none" in str(exc_info.value)


@pytest.mark.orm_base
def test_connection_string():
    assert dockv5_base.Base
    assert dockv5_base.engine
    assert dockv5_base.connection.begin()
    assert dockv5_base.session
    assert dockv5_base.session.close() == None
    assert dockv5_base.connection.close() == None
