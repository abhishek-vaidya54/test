"""Add column deleted_at in external_admin_users

Revision ID: 75e5f7db0893
Revises: 6babc516b4da
Create Date: 2021-06-30 12:36:34.540864

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "75e5f7db0893"
down_revision = "6babc516b4da"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "external_admin_user",
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_column("external_admin_user", "deleted_at")
