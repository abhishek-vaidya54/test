# Third Party Import
import pytest

# Local Application Import
from sat_orm.pipeline import Client

@pytest.mark.input_validation
def test_client_validate_name():
    ''' Validates client name column'''
    with pytest.raises(Exception) as exc_info:
        assert Client(name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_client_validate_prefix():
    ''' Validates client prefix column'''
    with pytest.raises(Exception) as exc_info:
        assert Client(prefix=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_client_validate_guid():
    ''' Validates client guid column'''
    with pytest.raises(Exception) as exc_info:
        assert Client(guid=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_client_validate_enable_processing():
    ''' Validates client enable_processing column'''
    with pytest.raises(Exception) as exc_info:
        assert Client(enable_processing=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.input_validation
def test_client_validate_dynamic_shift():
    ''' Validates client dynamic_shift column'''
    with pytest.raises(Exception) as exc_info:
        assert Client(dynamic_shift=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_return_type
def test_client_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    client = Client()
    assert isinstance(client.as_dict(),dict)

@pytest.mark.test_return_type
def test_client___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    client = Client()
    assert isinstance(client.__repr__(),str)
