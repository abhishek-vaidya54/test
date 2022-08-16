"""Add_utc_time_of_delivery

Revision ID: efe288a7721b
Revises: c4383cb72931
Create Date: 2022-08-09 16:35:18.454689

"""
from alembic import op
import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "efe288a7721b"
down_revision = "c4383cb72931"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("report_subscribe", "utc_time_of_delivery")
    op.add_column(
        "report_subscribe",
        sa.Column(
            "utc_time_of_delivery", sa.Time, default=datetime.time(), nullable=False
        ),
    )


def downgrade():
    op.drop_column("report_subscribe", "utc_time_of_delivery")
