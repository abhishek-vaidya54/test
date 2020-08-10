# Standard Library Imports
import datetime
import os
import json

# Third Party Imports
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, desc
from sqlalchemy.orm import relationship, validates

# Local Application Imports
from sat_orm.pipeline_orm.warehouse import Warehouse
from sat_orm.pipeline_orm.client import Client
from sat_orm.pipeline_orm.pipeline_base import Base


class ExternalAdminUser(Base):
    __tablename__ = "external_admin_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(255), nullable=False)
    username = Column(String(36), nullable=False)

    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    warehouse = relationship(Warehouse, backref=__tablename__)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    client = relationship(Client, backref=__tablename__)

    role = Column(String(20), nullable=True)

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

