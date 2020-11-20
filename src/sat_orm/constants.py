SUCCESS = {"status": "success", "data": []}

SUCCESS_DATA = {"id": None}

ERROR = {"status": "fail", "message": "", "errors": [], "code": 400}

ERROR_DATA = {"fieldName": "", "reason": ""}

ERROR_MULTIPLE_DATA = {"index": None, "errors": []}

MISSING_PARAMS_MESSAGE = "Parameters are missing."

INVALID_PARAMS_MESSAGE = "Errors in input fields."

INVALID_PARAM_LIMIT_MESSAGE = "Invalid limit parameter"

INVALID_PARAM_OFFSET_MESSAGE = "Invalid offset parameter"

INVALID_PARAM_SORT_MESSAGE = "Invalid sort parameter"

INVALID_PARAM_EXPAND_MESSAGE = "Invalid expand parameter"

INVALID_PARAM_USERNAME_MESSAGE = "Invalid external admin user"

INVALID_PARAM_SEX_MESSAGE = "Invalid sex"

MISSING_ID_MESSAGE = "Invalid ID"

INVALID_INTEGER_MESSAGE = "Invalid integer"

INVALID_FLOAT_MESSAGE = "Invalid float."

INVALID_DATE_MESSAGE = "Invalid date format."

MISSING_STRING_MESSAGE = "String cannot be empty."

INVALID_STRING_MESSAGE = "Invalid string. Only a-z, A-Z, 0-9, (, ), ., - is accepted. No spaces allowed at the start or end."

INVALID_BOOLEAN_MESSAGE = "Invalid boolean value."

INVALID_NAMES_LENGTH_MESSAGE = "Maximum of 70 characters for first and last name."

INVALID_JOB_FUNCTION_MESSAGE = "Invalid job function"

INVALID_SHIFT_MESSAGE = "Invalid shift"

INVALID_DUPLICATE_EXTERNAL_ID_MESSAGE = "Duplicate external ID."

INVALID_REQUEST = "Invalid request."

DUPLICATE_CLIENT_NAME_MESSAGE = "Client Name already exists."

INVALID_CLIENT_STATUS_MESSAGE = "Invalid client status."

INVALID_CLIENT_IA_NAME_FORMAT_MESSAGE = "Invalid client ia name format."

INVALID_WAREHOUSE_ID_MESSAGE = "Invalid warehouse ID."

INVALID_SETTINGS_ID_MESSAGE = "Invalid settings ID."

INVALID_CLIENT_ID_MESSAGE = "Invalid client ID."

INVALID_SHIFT_TIMEZONE_MESSAGE = "Invalid shift time zone."

INVALID_DOCK_PHASE_MESSAGE = "Invalid dock phase."

INVALID_DOCK_DEPLOYMENT_STAGE_MESSAGE = "Invalid dock deployment stage."

INVALID_DOCK_FIRMWARE_VERSION_MESSAGE = "Invalid dock firmware version."

EMPTY_STRING_ERROR_MESSAGE = "Param is empty or invalid."

INVALID_GROUP_ADMIN_MESSAGE = "Invalid group administrator."

NO_PERMISSION_MESSAGE = "You don't have the required permissions."

POLICY_POST_ERROR = "Error while saving the policy."

INVALID_ROLE_ERROR_MESSAGE = "Invalid role."

INVALID_RESOURCE_ERROR_MESSAGE = "Invalid resource."

INVALID_ACTION_ERROR_MESSAGE = "Invalid action."

BULK_UPLOAD_IN_PROGRESS_ERROR_MESSAGE = "Bulk upload is already in progress."

INVALID_EMAIL_ERROR_MESSAGE = "Invalid email address."

USER_NOT_FOUND_ERROR_MESSAGE = "User not found."

INVALID_EX_ADMIN_PUT_ACTION_ERROR_MESSAGE = "Action should be enable or disable."

EX_ADMIN_VALID_PUT_ACTIONS = ("enable", "disable")

INVALID_TARGET_TYPE_MESSAGE = (
    "target_type should be one of 'group', 'warehouse', 'industrial_athlete'"
)

VALID_TARGET_TYPES = ("group", "warehouse", "industrial_athlete")

INVALID_TARGET_ID_MESSAGE = "target_id should be id of target_type table"

VALID_SETTING_VALUE_OBJ = {
    "hapticEnabled": bool,
    "athleteEnabled": bool,
    "showEngagement": bool,
    "hapticBendNumber": int,
    "hapticFeedbackGap": int,
    "hapticBendPercentile": int,
    "hapticFeedbackWindow": int,
    "hapticSingleBendWindow": int,
    "hapticSagAngleThreshold": int,
    "showHapticModal": bool,
    "showBaselineModal": bool,
    "showSafetyScoreModal": bool,
    "handsFree": bool,
    "showSafetyJudgement": bool,
    "eulaVersion": int,
    "enagementEnabled": bool,
}

INVALID_SETTING_VALUE_OBJ_MESSAGE = "value object is not valid"


"""
    REGEX FOR DATA INPUT
"""
# ASCII equivalent of 0-9, A-Z, a-z, (, ), ., -
# No space at front or end
# REGEX_STRING = "^[\x30-\x39\x2d\x2e\x28-\x29\x41-\x5A\x61-\x7A]([\x30-\x39\x2d\x2e\x28-\x29\x41-\x5A\x61-\x7A\x20]*[\x30-\x39\x2d\x2e\x28-\x29\x41-\x5A\x61-\x7A])?$"

"""
    REGEX FOR DATA INPUT
    ASCII HEX Format
    \x30-\x39 = 0 - 9
    \x27-\x29 = ' ( )
    \x2d-\x2f = - . /
    \x41-\x5A = A - Z
    \x61-\x7A = a - z
    \x20 = SPACE
"""
# No space at front or end
REGEX_STRING = "^[\x30-\x39\x2d-\x2f\x27-\x29\x41-\x5A\x61-\x7A]([\x30-\x39\x2d-\x2f\x27-\x29\x41-\x5A\x61-\x7A\x20]*[\x30-\x39\x2d-\x2f\x27-\x29\x41-\x5A\x61-\x7A])?$"


EMAIL_REGEX = """^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""


VALID_CSV_STRING = """External ID,First Name,Last Name,Warehouse,Group,Job Function,Shift,Gender,Weight,Height,Hire Date,Termination Date\n
                        50000,Reuben,Jun Liang,Lynn,Zone 2 Pickers,Manager,First,f,0,0,06/26/2020,06/26/2020"""

INVALID_CSV_STRING_MISSING_HEADER = """First Name,Last Name,Warehouse,Group,Job Function,Shift,Gender,Weight,Height,Hire Date,Termination Date\n
                        Reuben,Jun Liang,Lynn,Zone 2 Pickers,Manager,First,f,0,0,06/26/2020,06/26/2020"""

"""
    Default /athletes (GET) sort param, if sort param is not present
    sort by firstName (asc), lastName (asc), id (asc)
    True = asc, False = desc
"""
DEFAULT_IA_SORT_PARAM = "firstName:asc,lastName:asc,id:asc"


LOGZIO_TOKEN = {
    "TEST": "tRAodYuUuxIPHqrbxWSfuIFKbBFHFhAM",
    "LIVE": "838879f3-1f84-4532-bb18-bc80eb0aa50c",
}

LOGZIO_REQUIRED_KEYS = [
    "username",
    "table",
    "action",
    "state_before",
    "state_after",
]

VALID_CLIENT_STATUSES = ("pilot", "deployment", "rollout", "inactive")

"""
    uppercase - all letters in capital
    capital - only the start letter in capital
    lowercase - all letters in small
"""
VALID_CLIENT_IA_NAME_FORMATS = (
    "FIRST_NAME_LAST_NAME",
    "FIRST_INITIAL_LAST_NAME",
    "ANONYMOUS",
)

VALID_SHIFT_TIMEZONES = ("US Eastern Time", "US Central Time")

VALID_DOCK_PHASES = ("DEPLOYED", "NOT DEPLOYED", "MAINTENANCE")

VALID_DOCK_DEPLOYMENT_STAGES = ("DEV", "PROD")

VALID_UPLOAD_TYPES = (
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

XLSX_FILE_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)


# --------- RBAC CONSTS
RBAC_VALID_ROLES = ("manager", "admin", "superuser")

CREATE_VALID_ROLES = ("manager", "admin")

RBAC_VALID_RESOURCES = (
    "athletes",
    "clients",
    "shifts",
    "docks",
    "warehouses",
    "jobfunctions",
    "roles",
    "bulkupload",
    "groups",
    "external_admin_user",
    "settings",
    "sensors",
)

RBAC_VALID_ACTIONS = ("read", "write", "update", "delete")

RBAC_ACTION_VALUES = {
    "read": "get",
    "write": "post",
    "update": "put",
    "delete": "delete",
}

RBAC_ACTION_KEYS = {"get": "read", "post": "write", "put": "update", "delete": "delete"}

METHOD_GET = "get"
METHOD_POST = "post"
METHOD_PUT = "put"
METHOD_DELETE = "delete"

POLICY_ATHLETES_OBJ = "athletes"
POLICY_CLIENTS_OBJ = "clients"
POLICY_SHIFTS_OBJ = "shifts"
POLICY_DOCKS_OBJ = "docks"
POLICY_WAREHOUSES_OBJ = "warehouses"
POLICY_JOBFUNCTIONS_OBJ = "jobfunctions"
POLICY_ROLES_OBJ = "roles"
POLICY_BULK_UPLOAD_OBJ = "bulkupload"
POLICY_GROUPS_OBJ = "groups"
POLICY_EXTERNAL_ADMIN_USER_OBJ = "external_admin_user"
POLICY_SETTINGS_OBJ = "settings"
POLICY_SENSORS_OBJ = "sensors"


# warehouse
INVALID_LAT_LONG_DIRECTION_MESSAGE = 'should be one of ("N", "S", "E", "W")'

INVALID_LAT_LONG_MESSAGE = {
    "latitude": "Latitude should be between -90 and 90",
    "longitude": "Longitude should be between -180 and 180",
}


IA_NAME_FORMAT_REGEX = {
    "FIRST_NAME_LAST_NAME": {
        "First Name": "^[a-z]+(?:[-.']?[a-z]+)*$",  # for maching strings with hyphen periods or single qoutes eg; a-a-aaaa-a
        "Last Name": "^[a-z]+(?:[ -.']?[a-z]+)*$",  # for maching strings with hyphen or periods or single qoutes or spaces eg; a-a-aa aa-a
    },
    "FIRST_INITIAL_LAST_NAME": {
        "First Name": "^[a-z]{1}.?$",  # for maching strings eg; t. or t
        "Last Name": "^[a-z]+(?:[ -.']?[a-z]+)*$",  # for maching strings with hyphen or periods or single qoutes or spaces eg; a-a-aa aa-a
    },
    "ANONYMOUS": {
        "First Name": "^[a-z0-9]+(?:[-.]?[a-z0-9]*)*$",  # for maching strings a12sa12
        "Last Name": "^[a-z0-9]+(?:[-.]?[a-z0-9]*)*$",  # for maching strings with hyphen eg; aa.aa
    },
}

IA_NAME_FORMATS = {
    "FIRST_NAME_LAST_NAME": "John Doe | John-Ken Ken-Doe | John Ken Doe",
    "FIRST_INITIAL_LAST_NAME": "J. Doe | J. Ken-Doe | J. Ken Doe",
    "ANONYMOUS": "XYZ 123",
}

INVALID_IA_NAME_FORMAT_MESSAGE = "Invalid First Name/Last Name format; should be : "
