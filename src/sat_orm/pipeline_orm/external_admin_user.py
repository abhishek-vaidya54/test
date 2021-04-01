# Standard Library Imports
import datetime

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, desc, event
from sqlalchemy.orm import relationship, validates

# Local Application Imports
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.user_warehouse_association import UserWarehouseAssociation
from sat_orm.pipeline_orm.user_role_association import UserRoleAssociation
from sat_orm.pipeline_orm.user_client_association import UserClientAssociation
from sat_orm.pipeline_orm.pipeline_base import Base
import sat_orm.constants as constants
from sat_orm.pipeline_orm.utilities import utils
from sat_orm.pipeline_orm.utilities import client_utils
from sat_orm.pipeline_orm.utilities import warehouse_utils
from sat_orm.pipeline_orm.utilities.utils import build_error, check_errors_and_return


class ExternalAdminUser(Base):
    __tablename__ = "external_admin_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    is_active = Column(String(5), server_default="true")

    #  Table relationships
    clients = relationship(UserClientAssociation, back_populates=__tablename__)
    warehouses = relationship(UserWarehouseAssociation, back_populates=__tablename__)
    roles = relationship(UserRoleAssociation, back_populates=__tablename__)

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

    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "db_created_at": self.db_created_at,
            "db_modified_at": self.db_modified_at,
        }

    def as_dict_camel_case(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }

    def __eq__(self, other):
        """
        Override the default equals behavior
        """
        return (
            self.id == other.id
            and self.email == other.email
            and self.username == other.username
            and self.db_created_at == other.db_created_at
            and self.db_modified_at == other.db_modified_at
        )

    @staticmethod
    def create(session, email, username, warehouse_id, client_id):
        external_admin_user = ExternalAdminUser(email=email, username=username)
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

    is_valid = utils.is_valid_email(email)
    if not is_valid:
        errors.append(build_error("email", constants.INVALID_EMAIL_ERROR_MESSAGE))

    check_errors_and_return(errors)
