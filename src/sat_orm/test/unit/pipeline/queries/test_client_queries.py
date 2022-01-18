import pytest
import sat_orm.pipeline_orm.queries.client_queries as client_queries


def test_get_client_by_id_success(get_external_admin_user, test_session):
    """
    Checks if method returns correct client
    Input:
        correct client id
    Output:
        correct client
    """
    client = client_queries.get_client_by_id(
        test_session, get_external_admin_user.client_id
    )
    assert client.id == get_external_admin_user.client_id


def test_get_client_by_id_failure(test_session):
    """
    Checks if method returns correct none
    Input:
        incorrect client id
    Output:
        None
    """
    invalid_int = 0
    client = client_queries.get_client_by_id(test_session, invalid_int)
    assert not client


def test_get_client_by_name_success(client_factory, test_session):
    """
    Checks if method returns correct client
    Input:
        correct client name
    Output:
        correct client
    """
    client = client_queries.get_client_by_name(test_session, client_factory.name)
    assert client.name == client_factory.name


def test_get_client_by_name_failure(invalid_string_space_front, test_session):
    """
    Checks if method returns correct none
    Input:
        incorrect client id
    Output:
        None
    """
    client = client_queries.get_client_by_name(test_session, invalid_string_space_front)
    assert not client
