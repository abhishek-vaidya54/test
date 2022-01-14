# Third Party Imports
import pytest

# Local Application Imports
from sat_orm.pipeline import Client
from sat_orm.pipeline import Warehouse


@pytest.mark.input_validation
def test_warehouse_validate_client_id():
    """Validate warehouse client_id Column"""
    with pytest.raises(Exception) as exc_info:
        assert Warehouse(client_id=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_warehouse_validate_name():
    """Validate warehouse name Column"""
    with pytest.raises(Exception) as exc_info:
        assert Warehouse(name=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_warehouse_validate_prefered_timezone():
    """Validate warehouse prefered_timezone Column"""
    with pytest.raises(Exception) as exc_info:
        assert Warehouse(prefered_timezone=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_warehouse_validate_display_names():
    """Validate warehouse display_names Column"""
    with pytest.raises(Exception) as exc_info:
        assert Warehouse(display_names=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_warehouse_validate_update_engagement():
    """Validate warehouse update_engagement Column"""
    with pytest.raises(Exception) as exc_info:
        assert Warehouse(update_engagement=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.test_return_type
def test_warehouse_as_dict_returns_dictionary():
    """Checks the return value of as_dict is a dictionary"""
    warehouse = Warehouse()
    assert isinstance(warehouse.as_dict(), dict)


@pytest.mark.test_return_type
def test_warehouse___repr___returns_string():
    """Checks the return value of __repr is a string"""
    warehouse = Warehouse()
    assert isinstance(warehouse.__repr__(), str)


@pytest.mark.relationships
def test_warehouse_client_relationship(session):
    """Test to see if client relationship works with warehouse client_id foreign key"""
    # TODO: add factory boy
    client = session.query(Client).filter_by(id=32).first()
    warehouse = client.warehouses[0]
    assert warehouse == session.query(Warehouse).filter_by(id=warehouse.id).first()
    warehouse = session.query(Warehouse).first()
    client = warehouse.client
    assert client.id != None
