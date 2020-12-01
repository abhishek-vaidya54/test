# Third Party Import
import pytest
import datetime
from sat_orm.pipeline_orm import client

@pytest.mark.input_validation
def test_client_validate_name():
    ''' Validates client name column'''
    with pytest.raises(Exception) as exc_info:
        assert client.Client(name=None)
    assert 'cannot be Null' in str(exc_info.value)

@pytest.mark.test_return_type
def test_client_as_dict_returns_dictionary():
    ''' Checks the return value of as_dict is a dictionary'''
    response = client.Client()
    assert isinstance(response.as_dict(),dict)

@pytest.mark.test_return_type
def test_client___repr___returns_string():
    ''' Checks the return value of __repr is a string'''
    response = client.Client()
    assert isinstance(response.__repr__(),str)

def test_client_insert_valid_new_id(valid_client_post_event, test_session):
    ''' Validates client insertion validations with new id'''
    valid_client_post_event["id"] = 100
    valid_client_post_event["enableProcessing"] = 1
    valid_client_post_event["status"] = 'deployment'
    response = client.insert(test_session, valid_client_post_event)
    assert isinstance(response, int)
    new_client = test_session.query(client.Client).filter_by(id=response).first()
    assert new_client.name == valid_client_post_event["name"]
    assert new_client.status == valid_client_post_event["status"]
    assert new_client.contracted_users == int(valid_client_post_event["contracted_users"])

def test_is_valid_insert_invalid(invalid_client_post_event, test_session):
    """
        Checks that it returns 0
        Input: 
            invalid_client_post_event: event that includes data with an old id
        return: 0
    """
    response = client.insert(test_session, invalid_client_post_event)
    assert response == 0

def test_client_update_valid(valid_client_put_event, test_session):
    ''' 
        Validates client updation validations
    '''
    valid_client_put_event["enableProcessing"] = 1
    response = client.update(test_session, valid_client_put_event)
    assert response
    assert isinstance(response, int)
    new_client = test_session.query(client.Client).filter_by(id=response).first()
    assert new_client.name == valid_client_put_event["name"]
    assert new_client.status == valid_client_put_event["status"]
    assert new_client.contracted_users == int(valid_client_put_event["contracted_users"])

def test_is_valid_update_invalid(invalid_client_put_event, test_session):
    """
        Checks that it returns False
        Input: 
            invalid_client_post_event: event that includes invalid data
        return: False
    """
    try:
        response = client.update(test_session, invalid_client_put_event)
    except Exception as e:
        response = False
    assert response == False

def test_client_delete_valid(valid_client_delete_event, test_session):
    ''' 
        Validates client deletion validations
    '''
    response = client.delete(test_session, valid_client_delete_event)
    assert response

def test_is_valid_update_invalid(invalid_client_delete_event, test_session):
    """
        Checks that it returns False
        Input: 
            invalid_client_post_event: event that includes invalid data
        return: False
    """
    response = client.delete(test_session, invalid_client_delete_event)
    assert response['error'] == 'Error deleting client'