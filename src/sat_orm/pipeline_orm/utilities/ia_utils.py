import re
from datetime import datetime, date
from sat_orm.pipeline_orm.queries import athlete_queries
from sat_orm.pipeline_orm.queries import client_queries
from sat_orm.pipeline_orm.queries import shift_queries
from sat_orm.pipeline_orm.queries import job_function_queries
from sat_orm.pipeline_orm.queries import warehouse_queries
from sat_orm.pipeline_orm.queries import setting_queries
import sat_orm.constants as constants


def is_valid_ia_first_last_name(connection, value, field, client_id):
    client = client_queries.get_client_by_id(connection, client_id)
    pattern = re.compile(
        constants.IA_NAME_FORMAT_REGEX[client.ia_name_format][field],
        flags=re.IGNORECASE,
    )
    is_valid = bool(re.match(pattern, value))
    if is_valid:
        return True, None

    return (
        False,
        (
            constants.INVALID_IA_NAME_FORMAT_MESSAGE
            + constants.IA_NAME_FORMATS[client.ia_name_format]
        ),
    )


def duplicate_external_id_with_termination_date(termination_date):
    return 'The user id that you are trying to add is already in use and has a termination date of '+str(termination_date)+'. Please specify a different user id.'


def is_valid_external_id(
    connection, external_id, warehouse_id, hire_date=None, ia=None, existing_ia_id=None
):
    """
    Validates an IA's external ID
    Checks if
        IA with the same warehouse ID & external ID is already in the database
    If an existing_ia_id is provided,
        if there is an IA with the same external id & both have same ID, then it is valid
        else not valid.
    Returns [True, None] if it is a valid external ID
    Returns [False, reason] if it is not
    """
    if ia:
        if str(external_id) == str(ia.external_id):
            return True, None

    existing_ia = athlete_queries.get_ia_by_external_id(
        connection, external_id, warehouse_id, hire_date
    )
    # DB does not contain any IA with the same external_id
    if existing_ia:
        # check if comparing against same IA
        if str(existing_ia_id) == str(existing_ia.id):
            return True, None
        if existing_ia.termination_date:
            return False, duplicate_external_id_with_termination_date(existing_ia.termination_date)
        else:
            return False, constants.DUPLICATE_EXTERNAL_ID_MESSAGE

    pattern = re.compile(constants.EXTERNAL_ID_REGEX, flags=re.IGNORECASE)
    if re.match(pattern, external_id):
        return True, external_id

    return False, constants.INVALID_EXTERNAL_ID_MESSAGE


def is_valid_client(connection, client_id):
    """
    Validates a client, checks if client belongs to the client
    Returns True if it is a valid client
    Returns False if it is not
    """
    client = client_queries.get_client_by_id(connection, client_id)
    return bool(client)


def is_valid_warehouse(connection, warehouse_id, client_id=None):
    """
    Validates a warehouse, checks if warehouse belongs to the client
    Returns True if it is a valid warehouse
    Returns False if it is not
    """
    warehouse = warehouse_queries.get_warehouse(
        connection, warehouse_id, client_id)
    return bool(warehouse)


def is_valid_setting(connection, settings_id):
    """
    Validates a warehouse, checks if warehouse belongs to the client
    Returns True if it is a valid warehouse
    Returns False if it is not
    """
    warehouse = setting_queries.get_setting(connection, settings_id)
    return bool(warehouse)


def is_valid_shift(connection, shift_id, warehouse_id):
    """
    Validates a shift, checks if shift belongs to the warehouse
    Returns True if it is a valid shift
    Returns False if it is not
    """

    shift = shift_queries.get_shift(connection, shift_id, warehouse_id)
    return bool(shift)


def is_valid_job_function(connection, job_function_id, warehouse_id):
    """
    Validates a job function, checks if job function belongs to the warehouse
    Returns True if it is a valid job function
    Returns False if it is not
    """

    job_function = job_function_queries.get_job_function(
        connection, job_function_id, warehouse_id
    )
    return bool(job_function)
