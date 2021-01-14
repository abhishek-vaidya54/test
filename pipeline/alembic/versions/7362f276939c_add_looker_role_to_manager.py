"""add looker role to manager

Revision ID: 7362f276939c
Revises: c09966f2898d
Create Date: 2021-01-05 12:46:49.036077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7362f276939c"
down_revision = "c09966f2898d"
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.execute(
    #     """
    #     INSERT INTO pipeline.casbin_rule
    #         (ptype, v0, v1, v2)
    #     VALUES
    #         ("p", "manager", "looker", "get"),
    #         ("p", "manager", "looker", "post"),
    #         ("p", "manager", "looker", "put"),
    #         ("p", "manager", "looker", "delete");
    #     """
    # )


def downgrade():
    op.execute("DELETE FROM pipeline.casbin_rule WHERE v0='manager' AND v1='looker';")
