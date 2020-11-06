"""add new unification permissions

Revision ID: b6978481f4b1
Revises: 5b04d0ebf898
Create Date: 2020-11-05 17:32:58.069313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = 'b6978481f4b1'
down_revision = 'cfafa0bc6498'
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

    for action in ["get", "post"]:
        records.append(CasbinRule(v0="superuser", v1="groups", v2=action))

    for action in ["get", "post", "put"]:
        records.append(CasbinRule(v0="superuser", v1="sensors", v2=action))

    for action in ["get", "post"]:
        records.append(CasbinRule(v0="superuser", v1="settings", v2=action))

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