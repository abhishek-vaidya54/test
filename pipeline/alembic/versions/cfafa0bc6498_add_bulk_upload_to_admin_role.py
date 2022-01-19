"""Add bulk upload to admin role.

Revision ID: cfafa0bc6498
Revises: c77a08526ef7
Create Date: 2020-11-02 21:26:35.421485

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = "cfafa0bc6498"
down_revision = "c77a08526ef7"
branch_labels = None
depends_on = None

Base = declarative_base()


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

    for action in ["get", "post", "put", "delete"]:
        records.append(CasbinRule(v0="admin", v1="bulk_upload", v2=action))

    records.append(CasbinRule(v0="admin", v1="clients", v2="get"))

    return records


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    records = build_records()

    session.add_all(records)
    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.query(CasbinRule).filter_by(v0="admin").filter_by(v1="bulk_upload").delete()
    session.query(CasbinRule).filter_by(v0="admin").filter_by(v1="clients").delete()

    session.commit()
    session.close()
