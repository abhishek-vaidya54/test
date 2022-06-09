from sat_orm.dockv5_orm.dockv5_base import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, event
from sqlalchemy.orm import relationship
import sat_orm.constants as constants
import sat_orm.pipeline_orm.utilities.firmware_utils as fu
import sat_orm.pipeline_orm.queries.firmware_queries as fq
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class Firmware(Base):
    __tablename__ = "firmware"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(255), nullable=False)
    s3_url = Column(String(255), nullable=True)
    hardware_id = Column(Integer, ForeignKey("hardware.id"), nullable=False)

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    hardware = relationship("Hardware", back_populates="firmwares")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "version": getattr(self, "version"),
            "s3_url": getattr(self, "s3_url"),
        }


@event.listens_for(Firmware, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single firmware
    Input:
        params_input: json containing data to be added for a single firmware.
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    # version = params_input.get("version", "")
    s3_url = params_input.get("s3_url", "")
    # device_type_id = params_input.get("device_type_id")
    # hardware_id = params_input.get("hardware_id")

    # is_valid = fu.is_non_empty_string(version)
    # if not is_valid:
    #     errors.append(build_error("version", constants.EMPTY_STRING_ERROR_MESSAGE))

    is_valid = fu.is_non_empty_string(s3_url)
    is_valid_url = False
    if fu.is_valid_url(s3_url):
        is_valid_url = True
    if not is_valid or not is_valid_url:
        errors.append(build_error("s3_url", constants.S3_EMPTY_STRING_ERROR_MESSAGE))

    # is_valid = fu.is_valid_device_type_id(connection, device_type_id)
    # if not is_valid:
    #     errors.append(
    #         build_error("device_type_id", constants.INVALID_DEVICE_TYPE_MESSAGE)
    #     )

    # is_valid = fu.is_valid_hardware_id(connection, hardware_id)
    # if not is_valid:
    #     errors.append(build_error("hardware_id", constants.INVALID_HARDWARE_MESSAGE))

    check_errors_and_return(errors)

    @event.listens_for(Firmware, "before_update")
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

        #     if "id" in params_input:
        #         is_valid = fq.get_firmware_exists(connection, params_input.get("id", ""))
        #         if not is_valid:
        #             errors.append(build_error("id", constants.INVALID_FIRMWARE_ID))

        #     if "version" in params_input:
        #         is_valid = fu.is_non_empty_string(params_input.get("version", ""))
        #         if not is_valid:
        #             errors.append(build_error("version", constants.EMPTY_STRING_ERROR_MESSAGE))

        if "s3_url" in params_input:
            is_valid = fu.is_non_empty_string(s3_url)
            is_valid_url = False
            if fu.is_valid_url(s3_url):
                is_valid_url = True
            if not is_valid or not is_valid_url:
                errors.append(
                    build_error("s3_url", constants.S3_EMPTY_STRING_ERROR_MESSAGE)
                )

    #     if "device_type_id" in params_input:
    #         is_valid = fu.is_valid_device_type_id(
    #             connection, params_input.get("device_type_id", "")
    #         )
    #         if not is_valid:
    #             errors.append(
    #                 build_error("device_type_id", constants.INVALID_DEVICE_TYPE_MESSAGE)
    #             )

    #     if "hardware_id" in params_input:
    #         is_valid = fu.is_valid_hardware_id(params_input.get("hardware_id", ""))
    #         if not is_valid:
    #             errors.append(
    #                 build_error("hardware_id", constants.INVALID_HARDWARE_MESSAGE)
    #             )

    check_errors_and_return(errors)
