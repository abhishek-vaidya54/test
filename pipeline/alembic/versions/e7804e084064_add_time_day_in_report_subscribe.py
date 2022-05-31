"""add_time_day_in_report_subscribe

Revision ID: e7804e084064
Revises: b48b02b5fcef
Create Date: 2022-05-20 13:03:05.135401

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "e7804e084064"
down_revision = "b48b02b5fcef"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "report_subscribe",
        sa.Column(
            "day_of_delivery",
            sa.Enum(
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "report_subscribe",
        sa.Column(
            "time_of_delivery",
            sa.Time,
            default=datetime.time(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("report_subscribe", "day_of_delivery")
    op.drop_column("report_subscribe", "time_of_delivery")
