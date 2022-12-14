"""
Author = Vincent Turnier
Created = September 13, 2019
Note:
    Make sure to checkout out database-models/wiki to learn more about testing
    link: https://github.com/strongarm-tech/database_models/wiki/Database-Testing

Description:
    The following test all the inputs of the config.py module. Checks to see if the
    inputes are validated. 
"""

import pytest

from sat_orm.dockv5 import Config, DockPhase
from sat_orm.dockv5_orm import config


@pytest.mark.input_validation
def test_config_dock_id_is_not_none():
    """Validates config dock_id column"""
    with pytest.raises(Exception) as exc_info:
        assert Config(dock_id=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_config_client_id_is_not_none():
    """Validates config client_id column"""
    with pytest.raises(Exception) as exc_info:
        assert Config(client_id=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_config_warehouse_id_is_not_none():
    """Validates config warehouse_id column"""
    with pytest.raises(Exception) as exc_info:
        assert Config(warehouse_id=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_config_deployment_stage_is_not_none():
    """Validates config deployment_stage column"""
    with pytest.raises(Exception) as exc_info:
        assert Config(deployment_stage=None)
    assert "cannot be Null" in str(exc_info.value)


@pytest.mark.input_validation
def test_config_barcode_regex_return_none_if_empty():
    """Checks to see if barcode_regex returns None or barcode_regex"""
    config = Config(barcode_regex="")
    assert config.barcode_regex == None
    config = Config(barcode_regex="123343")
    assert config.barcode_regex != None


@pytest.mark.input_validation
def test_config_deployment_stage_is_dev_or_prod():
    """Validates config deployment_stage enum values"""
    with pytest.raises(Exception) as exc_info:
        assert Config(deployment_stage="something")
    assert str(exc_info.value) == "deployment_stage can only be [dev,prod]"


@pytest.mark.test_return_type
def test_config_as_dict_returns_dictionary():
    """Checks the return value of as_dict is a dictionary"""
    config = Config()
    assert isinstance(config.as_dict(), dict)


@pytest.mark.test_return_type
def test_config___repr___returns_string():
    """Checks the return value of __repr is a string"""
    config = Config()
    assert isinstance(config.__repr__(), str)


# @pytest.mark.test_inserts
# def test_config_insert_or_update(session):
#     ''' checks to see if the row was updated or if a new row should be added'''
#     config.insert_or_update(session,data)
#     # TODO: Check to see if phase is poped out of data
#     # TODO: check to see if dock_id is not None
#     # TODO: if dock is in table, check to see if dock_id is poped out of data
#     # TODO: if dock is in table, check to see if table has been updated
#     # TODO: if dock is not in table, check to see if config is added to session
#     assert False
