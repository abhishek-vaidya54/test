import datetime
from sat_orm.dockv5_orm.dockv5_base import Base
from sat_orm.dockv5_orm.firmware_group_association import FirmwareGroupAssociation
from sqlalchemy import Column, String, Integer, DateTime, event
from sqlalchemy.orm import relationship
import sat_orm.constants as constants
import sat_orm.pipeline_orm.utilities.firmware_utils as fu
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class FirmwareGroup(Base):
    __tablename__ = "firmware_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    db_created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    firmwares = relationship(FirmwareGroupAssociation,
                             back_populates=__tablename__)

    configs = relationship("Config", back_populates="firmware_group")

    def as_dict(self):
        return {
            "id": getattr(self, "id"),
            "name": getattr(self, "name"),
            "description": getattr(self, "description"),
        }


# @event.listens_for(FirmwareGroup, "before_insert")
# def validate_before_insert(mapper, target):
#     """
#     Helper method to check if params are valid for adding a single firmware
#     Input:
#         params_input: json containing data to be added for a single firmware.
#     """
#     params_input = {}
#     for key, value in target.as_dict().items():
#         if value is not None:
#             params_input[key] = value
#     errors = []

#     name = params_input.get("name", "")
#     description = params_input.get("description", "")

#     is_valid = fu.is_non_empty_string(name)
#     if not is_valid:
#         errors.append(build_error("name", constants.EMPTY_STRING_ERROR_MESSAGE))

#     is_valid = fu.is_non_empty_string(description)
#     if not is_valid:
#         errors.append(build_error("description", constants.EMPTY_STRING_ERROR_MESSAGE))

#     check_errors_and_return(errors)


# @event.listens_for(FirmwareGroup, "before_update")
# def validate_before_update(mapper, target):
#     """
#     Helper method to check if params are valid for adding a single athlete
#     Input:
#         params_input: json containing data to be added for a single athlete.
#         warehouse_id: warehouse ID to validate job function
#     """
#     params_input = {}
#     for key, value in target.as_dict().items():
#         if value is not None:
#             params_input[key] = value
#     errors = []

#     if "name" in params_input:
#         is_valid = fu.is_non_empty_string(params_input.get("name", ""))
#         if not is_valid:
#             errors.append(build_error("name", constants.EMPTY_STRING_ERROR_MESSAGE))

#     if "description" in params_input:
#         is_valid = fu.is_non_empty_string(params_input.get("description", ""))
#         if not is_valid:
#             errors.append(
#                 build_error("description", constants.EMPTY_STRING_ERROR_MESSAGE)
#             )

#     check_errors_and_return(errors)
#     pass
