# Third Party Import
import pytest

# Local Application Imports
from sat_orm.pipeline import Client, Warehouse, ExternalAdminUser, UserRoleAssociation, UserWarehouseAssociation


@pytest.mark.input_validation
def test_external_admin_user_validate_email():
    """ Validates external admin user email column """
    with pytest.raises(Exception) as exc_info:
        assert ExternalAdminUser(email=None)
    assert "email cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_external_admin_user_validate_username():
    """ Validates external admin user username column """
    with pytest.raises(Exception) as exc_info:
        assert ExternalAdminUser(username=None)
    assert "username cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_external_admin_user_validate_client_id():
    """ Validates external admin user client_id column """
    with pytest.raises(Exception) as exc_info:
        assert ExternalAdminUser(client_id=None)
    assert "client_id cannot be Null" in str(exc_info.value)


@pytest.mark.test_return_type
def test_external_admin_user_as_dict_returns_dictionary():
    """ Checks the return value of as_dict is a dictionary"""
    user = ExternalAdminUser()
    assert isinstance(user.as_dict(), dict)


@pytest.mark.test_return_type
def test_external_admin_user___eq___returns_true(test_session, get_external_admin_user):
    """ Checks the return value of __eq__ is a True"""
    user = (
        test_session.query(ExternalAdminUser)
        .filter_by(id=get_external_admin_user.id)
        .first()
    )
    assert user.__eq__(get_external_admin_user)


@pytest.mark.relationships
def test_external_admin_user_client_relationship(test_session, get_external_admin_user):
    """ Test to see if relationship works correctly """
    user = (
        test_session.query(ExternalAdminUser)
        .filter_by(id=get_external_admin_user.id)
        .first()
    )
    client = test_session.query(Client).filter_by(id=user.client_id).first()
    assert client


@pytest.mark.relationships
def test_external_admin_user_warehouse_relationship(
    test_session, get_external_admin_user
):
    """ Test to see if relationship works correctly """
    user = (
        test_session.query(ExternalAdminUser)
        .filter_by(id=get_external_admin_user.id)
        .first()
    )
    warehouse = test_session.query(Warehouse).filter_by(id=user.warehouses[0].warehouse_id).first()
    assert warehouse


@pytest.mark.test_select
def test_create(test_session, get_external_admin_user):
    """
    verify get_by_id returns the correct object
    """
    user = ExternalAdminUser.get_by_id(test_session, get_external_admin_user.id)
    assert user


@pytest.mark.test_updates
def test_update_by_id(
    test_session, create_external_admin_user_params, get_external_admin_user
):
    """
    verify update_by_id updates the correct object
    """
    updated_user = ExternalAdminUser.update_by_id(
        test_session,
        get_external_admin_user.id,
        create_external_admin_user_params["email"],
        create_external_admin_user_params["username"],
    )

    user = (
        test_session.query(ExternalAdminUser)
        .filter_by(id=get_external_admin_user.id)
        .first()
    )

    assert user.email == updated_user.email
    assert user.username == updated_user.username


@pytest.mark.test_delete
def test_delete_by_id(test_session, get_external_admin_user):
    """
    verify delete_by_id deletes the correct object
    """
    test_session.query(UserRoleAssociation).filter_by(external_admin_user_id=get_external_admin_user.id).delete()
    test_session.query(UserWarehouseAssociation).filter_by(external_admin_user_id=get_external_admin_user.id).delete()
    test_session.commit()
    ExternalAdminUser.delete_by_id(test_session, get_external_admin_user.id)
    user = (
        test_session.query(ExternalAdminUser)
        .filter_by(id=get_external_admin_user.id)
        .first()
    )
    assert user is None