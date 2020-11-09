import copy
import sat_orm.constants as constants

def build_error(field_name, reason):
    error = copy.deepcopy(constants.ERROR_DATA)
    error["fieldName"] = field_name
    error["reason"] = reason
    return error