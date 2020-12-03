import pytest
from sat_orm.pipeline_orm.utilities import client_utils
import random
from sat_orm.constants import (
    VALID_CLIENT_IA_NAME_FORMATS)

def test_is_valid_client_status(client_factory, test_session):
    """
        Checks if is_valid_client_status method is returning True or not
        Input:
            client status
        Output:
            True
    """
    result = client_utils.is_valid_client_status(client_factory.status)
    assert result


def test_is_valid_client_ia_name_format():
    """
        Checks if is_valid_client_ia_name_format method is returning True or not
        Input:
            ia_name_format
        Output:
            True
    """
    result = client_utils.is_valid_client_ia_name_format(random.choice(VALID_CLIENT_IA_NAME_FORMATS))
    assert result

def test_is_valid_client_name(client_factory, test_session):
    """
        Checks if is_valid_client_name method is returning True or not
        Input:
            client name
        Output:
            True
    """
    result = client_utils.is_valid_client_name(test_session, client_factory.name)
    assert result