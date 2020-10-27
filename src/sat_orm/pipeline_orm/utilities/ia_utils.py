import re
from datetime import datetime, date
from sat_orm.pipeline_orm.queries import athlete_queries
from sat_orm.pipeline_orm.queries import client_queries
from sat_orm.pipeline_orm.queries import shift_queries
from sat_orm.pipeline_orm.queries import job_function_queries
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


def is_valid_external_id(connection, ia, external_id, existing_ia_id=None):
    """
    Validates an IA's external ID
    Checks if
        it is an int &
        an IA with the same client ID & external ID is already in the database
    If an existing_ia_id is provided,
        if there is an IA with the same external id & both have same ID, then it is valid
        else not valid.
    Returns [True, None] if it is a valid external ID
    Returns [False, reason] if it is not
    """
    if ia and str(external_id) == str(ia.external_id):
        return True, None

    existing_ia = athlete_queries.get_ia_by_external_id(
        connection, external_id, ia.warehouse_id
    )
    if not existing_ia:  # DB does not contain any IA with the same external_id
        return True, None
    if existing_ia_id and str(existing_ia_id) == str(
        existing_ia.id
    ):  # DB contains an IA with the same external_id, check if comparing against same IA
        return True, None
    return (
        False,
        constants.INVALID_DUPLICATE_EXTERNAL_ID_MESSAGE,
    )  # DB contains an IA with same external_id, but not comparing against the same IA.


def is_valid_date(date_input):
    """
    Helper method to check if input is a valid date (MM/dd/YY)
    Returns True if it is a valid date
    Returns False if it is not a valid date
    """
    try:
        if isinstance(date_input, datetime) or isinstance(date_input, date):
            return True, date_input
        if date_input is None:
            raise ValueError()
        date_str = str(datetime.strptime(date_input, "%m/%d/%Y").date())
        return True, date_str
    except ValueError:
        return False, None


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
