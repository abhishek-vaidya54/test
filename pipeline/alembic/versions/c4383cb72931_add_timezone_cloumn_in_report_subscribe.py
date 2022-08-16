"""Add_timezone_cloumn_in_report_subscribe

Revision ID: c4383cb72931
Revises: 8fd6a7a1336c
Create Date: 2022-08-08 15:44:33.722179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c4383cb72931"
down_revision = "8fd6a7a1336c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "report_subscribe",
        sa.Column("timezone", sa.String(length=30), nullable=False),
    )


def downgrade():
    op.drop_column("report_subscribe", "timezone")
