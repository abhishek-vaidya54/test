import copy
import json

from sqlalchemy import Column, Integer, String, JSON, DateTime, event
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

# Local Application Imports
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities.utils import build_error


class Groups(Base):
    __tablename__ = "groups"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    description = Column(String(45), nullable=True)
    db_created_at = Column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    override_settings = Column(TINYINT(1), nullable=False)

    # Table Relationships
    industrial_athletes = relationship("IndustrialAthlete", back_populates="groups")

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "db_created_at": self.db_created_at,
            "overrideSettings": self.override_settings,
        }

    def __repr__(self):
        return str(self.as_dict())


@event.listens_for(Groups, "before_insert")
def validate_before_insert(mapper, connection, target):
    """
    Helper method to check if params are valid for adding a single group
    Input:
        params_input: json containing data to be added for a single group.
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    for key in ["title", "description"]:
        is_valid, message = utils.is_valid_string(params_input.get(key, ""))
        if not is_valid:
            errors.append(build_error(key, message))

    is_valid, message = utils.is_valid_bool(params_input.get("overrideSettings", False))
    if not is_valid:
        errors.append(build_error("overrideSettings", message))

    if len(errors) > 0:
        error_response = copy.deepcopy(constants.ERROR)
        error_response["message"] = constants.INVALID_PARAMS_MESSAGE
        error_response["errors"] = errors
        raise Exception(json.dumps(error_response))