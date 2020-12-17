"""add role for users

Revision ID: 589cabbef055
Revises: e618e32273b3
Create Date: 2020-12-10 18:45:44.909655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = '589cabbef055'
down_revision = 'e618e32273b3'
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
    session.query(CasbinRule).filter_by(v0="superuser").filter_by(
        v1="external_admin_user"
    ).delete()
    session.query(CasbinRule).filter_by(v0="superuser").filter_by(
        v1="user"
    ).delete()
    records = [
        CasbinRule(v0="superuser", v1="users", v2=action)
        for action in ["get", "post", "put"]
    ]
    session.add_all(records)
    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(CasbinRule).filter_by(v0="superuser").filter_by(v1="users").delete()
    session.query(CasbinRule).filter_by(v0="superuser").filter_by(v1="external_admin_user").delete()
    records = [
        CasbinRule(v0="superuser", v1="external_admin_user", v2=action)
        for action in ["get", "post", "put", "delete"]
    ]
    session.add_all(records)
    session.commit()
    session.close()
