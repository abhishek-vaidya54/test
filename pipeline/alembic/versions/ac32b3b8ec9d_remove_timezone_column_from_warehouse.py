"""remove timezone column from warehouse

Revision ID: ac32b3b8ec9d
Revises: 1d714a7e2b53
Create Date: 2021-03-03 15:06:00.223386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ac32b3b8ec9d"
down_revision = "1d714a7e2b53"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("warehouse", "timezone")


def downgrade():
    op.add_column(
        "warehouse",
        sa.Column("timezone", sa.String(50), server_default="UTC", nullable=False),
    )
