# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    PrimaryKeyConstraint,
    Enum,
    VARCHAR,
    event,
)

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
import sat_orm.pipeline_orm.utilities.firmware_notification_utils as nu
import sat_orm.pipeline_orm.queries.firmware_notification_queries as nq
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class Notification(Base):
    __tablename__ = "notification"

    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    type = Column(
        Enum("update", "news", "warning", "event"),
        nullable=False,
        default="news",
    )
    url = Column(String(255), nullable=False)
    created_by = Column(
        Integer, ForeignKey("external_admin_user.id"), nullable=False
    )
    is_active = Column(Boolean, nullable=True, default=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    # Table Constraints
    PrimaryKeyConstraint("id")

    def as_dict(self):
        return {
            "id": self.id,
            "created_by": self.created_by,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "url": self.url,
            "is_active": self.is_active,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

@event.listens_for(Notification, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single notification
    Input:
        params_input: json containing data to be added for a single notification.
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    title = params_input.get("title", "")
    description = params_input.get("description", "")
    type = params_input.get("type", "")
    url = params_input.get("url", "")
    created_by = params_input.get("created_by")
    is_active = params_input.get("is_active")

    is_valid = nu.is_non_empty_string(title)
    if not is_valid:
        errors.append(build_error(
            "title", constants.EMPTY_STRING_ERROR_MESSAGE))
    
    is_valid = nu.is_non_empty_string(description)
    if not is_valid:
        errors.append(build_error(
            "description", constants.EMPTY_STRING_ERROR_MESSAGE))

    is_valid = nu.is_valid_type(type)
    if not is_valid:
        errors.append(build_error(
            "type", constants.INVALID_FIRMWARE_NOTIFICATION_TYPE_MESSAGE))

    is_valid = nu.is_non_empty_string(url)
    if not is_valid:
        errors.append(build_error(
            "url", constants.EMPTY_STRING_ERROR_MESSAGE))

    is_valid = nu.is_valid_created_by(connection, created_by)
    if not is_valid:
        errors.append(build_error(
            "created_by", constants.INVALID_CREATED_BY_MESSAGE))

    is_valid = nu.is_valid_is_active(is_active)
    if not is_valid:
        errors.append(
            build_error(
                "is_active", constants.INVALID_IS_ACTIVE_MESSAGE
            )
        )

    check_errors_and_return(errors)


@event.listens_for(Notification, "before_update")
def validate_before_update(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single athlete
    Input:
        params_input: json containing data to be added for a single athlete.
        warehouse_id: warehouse ID to validate job function
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    if "id" in params_input:
        is_valid = nq.get_firmware_notification_exists(
            connection,params_input.get("id", ""))
        if not is_valid:
            errors.append(build_error(
                "id", constants.INVALID_NOTIFICATION_ID))

    if "title" in params_input:
        is_valid = nu.is_non_empty_string(
            params_input.get("title", ""))
        if not is_valid:
            errors.append(build_error(
                "title", constants.EMPTY_STRING_ERROR_MESSAGE))

    if "description" in params_input:
        is_valid = nu.is_non_empty_string(
            params_input.get("description", ""))
        if not is_valid:
            errors.append(build_error(
                "phase", constants.EMPTY_STRING_ERROR_MESSAGE))

    if "type" in params_input:
        is_valid = nu.is_valid_type(
            params_input.get("type", ""))
        if not is_valid:
            errors.append(build_error(
                "type", constants.INVALID_FIRMWARE_NOTIFICATION_TYPE_MESSAGE))

    if "url" in params_input:
        is_valid = nu.is_non_empty_string(
            params_input.get("url", ""))
        if not is_valid:
            errors.append(build_error(
                "url", constants.EMPTY_STRING_ERROR_MESSAGE))

    if "created_by" in params_input:
        is_valid = nu.is_valid_created_by(
            connection,params_input.get("created_by", "")
        )
        if not is_valid:
            errors.append(
                build_error(
                    "created_by", constants.INVALID_CREATED_BY_MESSAGE
                )
            )
    
    if "is_active" in params_input:
        is_valid = nu.is_valid_is_active(
            params_input.get("is_active", ""))
        if not is_valid:
            errors.append(build_error(
                "is_active", constants.INVALID_IS_ACTIVE_MESSAGE))

    check_errors_and_return(errors)
    pass