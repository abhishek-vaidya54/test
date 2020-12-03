"""add app_restart_at to warehouse table

Revision ID: c9e1ef236af0
Revises: deedee498933
Create Date: 2020-12-03 19:10:21.885261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c9e1ef236af0"
down_revision = "deedee498933"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("warehouse", sa.Column("app_restart_at", sa.DateTime, nullable=True))


def downgrade():
    op.drop_column("warehouse", "app_restart_at")
