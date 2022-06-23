"""add_soft_delete_in_firmware_group

Revision ID: f5da1c70f358
Revises: ecb7e73f534c
Create Date: 2022-06-07 16:45:28.140409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f5da1c70f358"
down_revision = "ecb7e73f534c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "firmware_group",
        sa.Column("status", sa.String(length=90), server_default="active"),
    )
    op.add_column(
        "firmware_group",
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_column("firmware_group", "status")
    op.drop_column("firmware_group", "deleted_at")
