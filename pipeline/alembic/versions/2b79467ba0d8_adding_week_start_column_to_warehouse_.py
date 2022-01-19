"""adding week start column to warehouse table

Revision ID: 2b79467ba0d8
Revises: 0f8920768d73
Create Date: 2018-07-16 17:46:17.955397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2b79467ba0d8"
down_revision = "0f8920768d73"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column(
            "week_start", sa.Unicode(length=45), nullable=True, server_default="Sunday"
        ),
    )


def downgrade():
    op.drop_column("warehouse", "week_start")
