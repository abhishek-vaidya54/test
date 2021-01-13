import pytest
from sat_orm.pipeline_orm.utilities import ia_utils
from sat_orm.pipeline_orm.industrial_athlete import IndustrialAthlete

def test_is_valid_ia_first_name_valid(valid_ia_put_body, test_session):
    """
        Checks if is_valid_ia_first_last_name method is returning True or not
        Input:
            value of ia first name, field as "First Name" and client id 
        Output:
            True
    """
    result = ia_utils.is_valid_ia_first_last_name(test_session, valid_ia_put_body["firstName"], "First Name" , valid_ia_put_body["clientId"])
    assert result


def test_is_valid_ia_first_name_invalid(invalid_athletes_put_body_invalid_first_name, test_session):
    """
        Checks if is_valid_ia_first_last_name method is returning False or not
        Input:
            invalid value of ia first name, field as "First Name" and client id 
        Output:
            False
    """
    result = ia_utils.is_valid_ia_first_last_name(test_session, invalid_athletes_put_body_invalid_first_name["firstName"], "First Name" , invalid_athletes_put_body_invalid_first_name["clientId"])
    assert result[0] == False

def test_is_valid_ia_last_name_valid(valid_ia_put_body, test_session):
    """
        Checks if is_valid_ia_first_last_name method is returning True or not
        Input:
            value of ia last name, field as "Last Name" and client id 
        Output:
            True
    """
    result = ia_utils.is_valid_ia_first_last_name(test_session, valid_ia_put_body["lastName"], "Last Name" , valid_ia_put_body["clientId"])
    assert result

def test_is_valid_ia_last_name_invalid(invalid_athletes_put_body_invalid_last_name, test_session):
    """
        Checks if is_valid_ia_first_last_name method is returning False or not
        Input:
            invalid value of ia last name, field as "Last Name" and client id 
        Output:
            False
    """
    result = ia_utils.is_valid_ia_first_last_name(test_session, invalid_athletes_put_body_invalid_last_name["lastName"], "Last Name" , invalid_athletes_put_body_invalid_last_name["clientId"])
    assert result[0] == False

def test_is_valid_external_id_valid(get_external_admin_user, test_session):
    """
        Checks if is_valid_external_id method is returning True or not
        Input:
            ia row, ia external id and ia row id 
        Output:
            True
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_external_id(test_session, ia, ia.external_id , ia.id)
    assert result

def test_is_valid_external_id_invalid(get_external_admin_user,invalid_string_space_front, test_session):
    """
        Checks if is_valid_external_id method is returning False or not
        Input:
            ia row, invalid_string_space_front and ia row id 
        Output:
            False
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_external_id(test_session, ia, invalid_string_space_front , ia.id)
    assert result


def test_is_valid_client_valid(get_external_admin_user, test_session):
    """
        Checks if is_valid_client method is returning True or not
        Input:
            client id
        Output:
            True
    """
    
    result = ia_utils.is_valid_client(test_session, get_external_admin_user.client_id)
    assert result

def test_is_valid_client_invalid(invalid_id, test_session):
    """
        Checks if is_valid_client method is returning False or not
        Input:
            invalid_id
        Output:
            False
    """
    
    result = ia_utils.is_valid_client(test_session, invalid_id)
    assert result == False

def test_is_valid_warehouse_valid(get_external_admin_user, test_session):
    """
        Checks if is_valid_warehouse method is returning True or not
        Input:
            warehouse_id
        Output:
            True
    """
    
    result = ia_utils.is_valid_warehouse(test_session, get_external_admin_user.warehouse_id)
    assert result

def test_is_valid_warehouse_invalid(invalid_id, test_session):
    """
        Checks if is_valid_warehouse method is returning False or not
        Input:
            invalid_id
        Output:
            False
    """
    
    result = ia_utils.is_valid_warehouse(test_session, invalid_id)
    assert result == False

def test_is_valid_setting_valid(settings_factory, test_session):
    """
        Checks if is_valid_setting method is returning True or not
        Input:
            setting_id
        Output:
            True
    """
    result = ia_utils.is_valid_setting(test_session,settings_factory.id)
    assert result

def test_is_valid_setting_invalid(invalid_id, test_session):
    """
        Checks if is_valid_setting method is returning False or not
        Input:
            invalid_id
        Output:
            False
    """
    
    result = ia_utils.is_valid_setting(test_session, invalid_id)
    assert result == False

def test_is_valid_shift_valid(get_external_admin_user, test_session):
    """
        Checks if is_valid_shift method is returning True or not
        Input:
            shift_id, warehouse_id
        Output:
            True
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_shift(test_session,ia.shift_id, ia.warehouse_id)
    assert result

def test_is_valid_shift_invalid_shift_id(invalid_id, get_external_admin_user, test_session):
    """
        Checks if is_valid_shift method is returning False or not
        Input:
            invalid_id, shift_id
        Output:
            False
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_shift(test_session, invalid_id, ia.warehouse_id)
    assert result == False

def test_is_valid_shift_invalid_warehouse_id(invalid_id, get_external_admin_user, test_session):
    """
        Checks if is_valid_shift method is returning False or not
        Input:
            invalid_id, warehouse_id
        Output:
            False
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_shift(test_session, ia.shift_id, invalid_id)
    assert result == False

def test_is_valid_job_function_valid(get_external_admin_user, test_session):
    """
        Checks if is_valid_job_function method is returning True or not
        Input:
            setting_id
        Output:
            True
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_job_function(test_session, ia.job_function_id, ia.warehouse_id)
    assert result

def test_is_valid_job_function_invalid_job_function_id(invalid_id, get_external_admin_user, test_session):
    """
        Checks if is_valid_job_function method is returning False or not
        Input:
            invalid_id, warehouse_id
        Output:
            False
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_job_function(test_session, invalid_id, ia.warehouse_id)
    assert result == False

def test_is_valid_job_function_invalid_warehouse_id(invalid_id, get_external_admin_user, test_session):
    """
        Checks if is_valid_job_function method is returning False or not
        Input:
            job_function_id, invalid_id
        Output:
            False
    """
    ia = test_session.query(IndustrialAthlete).first()
    result = ia_utils.is_valid_job_function(test_session, ia.job_function_id, invalid_id)
    assert result == False