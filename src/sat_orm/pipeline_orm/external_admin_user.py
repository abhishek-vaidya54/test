# Standard Library Imports
import datetime
import copy
import json

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, desc, event
from sqlalchemy.orm import relationship, validates

# Local Application Imports
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants 
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import client_utils
from sat_orm.pipeline_orm.utilities import warehouse_utils


class ExternalAdminUser(Base):
    __tablename__ = "external_admin_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(255), nullable=False)
    username = Column(String(36), nullable=False)

    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    warehouse = relationship(Warehouse, backref=__tablename__)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    client = relationship(Client, backref=__tablename__)

    role = Column(String(20), nullable=True, server_default="manager")
    is_active = Column(String(5), server_default="true")

    db_created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    db_modified_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    @validates("email")
    def validate_email(self, key, email):
        if email == None:
            raise Exception("email cannot be Null")
        else:
            return email

    @validates("username")
    def validate_username(self, key, username):
        if username == None:
            raise Exception("username cannot be Null")
        else:
            return username

    @validates("warehouse_id")
    def validate_warehouse_id(self, key, warehouse_id):
        if warehouse_id == None:
            raise Exception("warehouse_id cannot be Null")
        else:
            return warehouse_id

    @validates("client_id")
    def validate_client_id(self, key, client_id):
        if client_id == None:
            raise Exception("client_id cannot be Null")
        else:
            return client_id

    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "warehouse_id": self.warehouse_id,
            "client_id": self.client_id,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    def as_dict_camel_case(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "warehouseId": self.warehouse_id,
            "clientId": self.client_id,
        }

    def __eq__(self, other):
        """
        Override the default equals behavior
        """
        return (
            self.id == other.id
            and self.email == other.email
            and self.username == other.username
            and self.warehouse_id == other.warehouse_id
            and self.client_id == other.client_id
            and self.db_created_at == other.db_created_at
            and self.db_modified_at == other.db_modified_at
        )

    @staticmethod
    def create(session, email, username, warehouse_id, client_id):
        external_admin_user = ExternalAdminUser(
            email=email,
            username=username,
            warehouse_id=warehouse_id,
            client_id=client_id,
        )
        session.add(external_admin_user)
        session.commit()
        session.refresh(external_admin_user)
        return external_admin_user

    @staticmethod
    def get_by_id(session, id):
        external_admin_user = session.query(ExternalAdminUser).filter_by(id=id).first()
        return external_admin_user

    @staticmethod
    def update_by_id(
        session, id, email=None, username=None, warehouse_id=None, client_id=None
    ):
        external_admin_user = ExternalAdminUser.get_by_id(session, id)
        if email is not None:
            external_admin_user.email = email
        if username is not None:
            external_admin_user.username = username
        if warehouse_id is not None:
            external_admin_user.warehouse_id = warehouse_id
        if client_id is not None:
            external_admin_user.client_id = client_id

        session.commit()
        session.refresh(external_admin_user)
        return external_admin_user

    @staticmethod
    def delete_by_id(session, id):
        external_admin_user = ExternalAdminUser.get_by_id(session, id)
        session.delete(external_admin_user)
        session.commit()


@event.listens_for(ExternalAdminUser, "before_insert")
def validate_role_before_insert(mapper, connection, target):
    """
    Event hook method that fires before insert 
    to check if params are valid for inserting a single external_admin_user
    """
    params_input = {}
    for key, value in target.as_dict().items():
        if value is not None:
            params_input[key] = value
    errors = []

    email = params_input.get("email", "").lower()
    client_id = params_input.get("client_id", "")
    warehouse_id = params_input.get("warehouse_id", "")
    role = params_input.get("role", "")

    is_valid = utils.is_valid_email(email)
    if not is_valid:
        errors.append(utils.build_error("email", constants.INVALID_EMAIL_ERROR_MESSAGE))

    is_valid = client_utils.is_valid_client_id(connection, client_id)
    if not is_valid:
        errors.append(utils.build_error("client_id", constants.INVALID_CLIENT_ID_MESSAGE))

    is_valid = warehouse_utils.is_valid_warehouse(connection, warehouse_id, client_id)
    if not is_valid:
        errors.append(utils.build_error("warehouse_id", constants.INVALID_WAREHOUSE_ID_MESSAGE))

    if role:
        is_valid = role in constants.CREATE_VALID_ROLES
        if not is_valid:
            errors.append(utils.build_error("role", constants.INVALID_ROLE_ERROR_MESSAGE))

    if len(errors) > 0:
        error_response = copy.deepcopy(constants.ERROR)
        error_response["message"] = constants.INVALID_PARAMS_MESSAGE
        error_response["errors"] = errors
        raise Exception(json.dumps(error_response))

@event.listens_for(ExternalAdminUser, "before_update")
def validate_role_before_update(mapper, connection, target):
    """
    Event hook method that fires before role update to check if 
    role is valid
    """
    errors = []

    is_valid = target.role in constants.RBAC_VALID_ROLES
    if not is_valid:
        errors.append(utils.build_error("role", constants.INVALID_ROLE_ERROR_MESSAGE))

    if len(errors) > 0:
        error_response = copy.deepcopy(constants.ERROR)
        error_response["message"] = constants.INVALID_PARAMS_MESSAGE
        error_response["errors"] = errors
        raise Exception(json.dumps(error_response))
