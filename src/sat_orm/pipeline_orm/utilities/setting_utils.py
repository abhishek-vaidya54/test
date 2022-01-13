import sat_orm.constants as constants
from sat_orm.pipeline_orm.queries import setting_queries
from sat_orm.pipeline_orm.utilities.utils import build_error


def is_valid_target_type(target_type):
    """
    Helper method to check if input is a valid datetime
    Returns True if it is a valid datetime
    Returns False if it is not a valid datetime
    """
    return target_type in constants.VALID_TARGET_TYPES


def is_valid_target_id(connection, target_type, target_id):
    try:
        target = setting_queries.get_target_by_id(connection, target_type, target_id)
        if target:
            return True, None

        return False, constants.INVALID_TARGET_ID_MESSAGE
    except:
        return False, constants.INVALID_TARGET_ID_MESSAGE


def is_valid_value_obj(value):
    errors = []
    valid_obj = constants.VALID_SETTING_VALUE_OBJ
    all_keys = valid_obj.keys()
    # check if received object has all required keys
    have_all_keys = set(all_keys) == set(value.keys())
    if not have_all_keys:
        return False, constants.INVALID_SETTING_VALUE_OBJ_MESSAGE

    for key in value.keys():
        if key == "eulaVersion" and (
            isinstance(value[key], valid_obj[key]) or (value[key] is None)
        ):
            # Skip type check for Eula Version if the input is valid number or None
            continue
        elif not isinstance(value[key], valid_obj[key]):
            errors.append(build_error(key, "Should be %s" % valid_obj[key]))

    if errors:
        return False, errors

    return True, None
