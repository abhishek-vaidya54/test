"""add app_restart_at to warehouse table

Revision ID: c9e1ef236af0
Revises: deedee498933
Create Date: 2020-12-03 19:10:21.885261

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "c9e1ef236af0"
down_revision = "02dea1080340"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column(
            "app_restart_at",
            sa.DateTime,
            server_default=str(
                datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            ),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("warehouse", "app_restart_at")
