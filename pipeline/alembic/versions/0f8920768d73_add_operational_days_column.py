"""add operational days column

Revision ID: 0f8920768d73
Revises: 
Create Date: 2018-07-12 13:23:29.973723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0f8920768d73"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column(
            "utc_op_day_start",
            sa.Unicode(length=45),
            nullable=True,
            server_default="00:00:00",
        ),
    )


def downgrade():
    op.drop_column("warehouse", "utc_op_day_start")
