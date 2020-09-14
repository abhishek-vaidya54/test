"""add superuser role

Revision ID: d9d26752ef2b
Revises: b38403920c58
Create Date: 2020-09-09 13:15:13.706741

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InternalError

RBAC_VALID_RESOURCES = (
    "athletes",
    "clients",
    "shifts",
    "docks",
    "warehouses",
    "jobfunctions",
    "roles",
    "bulkupload",
)

ADMIN_RESOURCES = {
    "athletes": ["get", "post", "put", "delete"],
    "bulkupload": ["get", "post", "put", "delete"],
    "clients": ["get", "post", "put", "delete"],
    "shifts": ["get"],
    "jobfunctions": ["get"],
}


RBAC_ACTION_KEYS = {"get": "read", "post": "write", "put": "update", "delete": "delete"}

Base = declarative_base()


# revision identifiers, used by Alembic.
revision = "d9d26752ef2b"
down_revision = "b38403920c58"
branch_labels = None
depends_on = None


class CasbinRule(Base):
    __tablename__ = "casbin_rule"

    id = sa.Column(sa.Integer, primary_key=True)
    ptype = sa.Column(sa.String(length=255), nullable=True, default="p")
    v0 = sa.Column(sa.String(length=255), nullable=True)
    v1 = sa.Column(sa.String(length=255), nullable=True)
    v2 = sa.Column(sa.String(length=255), nullable=True)
    v3 = sa.Column(sa.String(length=255), nullable=True)
    v4 = sa.Column(sa.String(length=255), nullable=True)
    v5 = sa.Column(sa.String(length=255), nullable=True)


def build_records():
    records = []
    for resource in RBAC_VALID_RESOURCES:
        for action in list(RBAC_ACTION_KEYS.keys()):
            records.append(CasbinRule(v0="superuser", v1=resource, v2=action))
            if resource in ("athletes", "bulkupload"):
                records.append(CasbinRule(v0="manager", v1=resource, v2=action))
            if resource in ADMIN_RESOURCES:
                if action in ADMIN_RESOURCES[resource]:
                    records.append(CasbinRule(v0="admin", v1=resource, v2=action))
    return records


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    records = build_records()
    try:
        CasbinRule.__table__.create(bind)
    except InternalError as e:
        code = str(e.__dict__["orig"]).split("(")[1].split(",")[0]
        if code == "1050":
            session.query(CasbinRule).delete()
    finally:
        session.add_all(records)
        session.commit()
        session.close()


def downgrade():
    op.drop_table("casbin_rule")
