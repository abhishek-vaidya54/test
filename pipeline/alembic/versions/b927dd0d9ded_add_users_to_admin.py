"""add users to admin

Revision ID: b927dd0d9ded
Revises: 589cabbef055
Create Date: 2020-12-10 19:03:51.872308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = 'b927dd0d9ded'
down_revision = '589cabbef055'
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


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    records = []

    for action in ["get", "post", "put"]:
        records.append(CasbinRule(v0="admin", v1="users", v2=action))

    records.append(CasbinRule(v0="admin", v1="roles", v2="get"))
    records.append(CasbinRule(v0="admin", v1="warehouses", v2="get"))

    session.add_all(records)
    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(CasbinRule).filter_by(v0="admin").filter_by(v1="users").delete()
    session.query(CasbinRule).filter_by(v0="admin").filter_by(v1="roles").delete()
    session.query(CasbinRule).filter_by(v0="admin").filter_by(v1="warehouses").delete()

    session.commit()
    session.close()