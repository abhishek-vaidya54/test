from sat_orm.pipeline_orm.utilities import job_function_utils

def test_is_valid_group_admin_valid(valid_email):
    """
    checks if function returns true for a valid group admin
    """
    assert job_function_utils.is_valid_group_admin(valid_email)


def test_is_valid_group_admin_invalid(invalid_int):
    """
    checks if function returns true for an invalid group admin
    """
    assert job_function_utils.is_valid_group_admin(invalid_int)
