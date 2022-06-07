"""report_subscribe_shift_association

Revision ID: 894d3085db43
Revises: 98132a42c813
Create Date: 2022-05-31 11:22:31.063746

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "894d3085db43"
down_revision = "98132a42c813"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "report_subscribe_shift_association",
        sa.Column(
            "report_subscribe_id", sa.Integer(), nullable=False, primary_key=True
        ),
        sa.Column("shift_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_modified_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        # sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["report_subscribe_id"],
            ["report_subscribe.id"],
            name="fk_report_subscribe_shift_assoc_report_subscribe",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["shift_id"],
            ["shifts.id"],
            name="fk_report_subscribe_shift_assoc_shift",
            ondelete="CASCADE",
        ),
    )


def downgrade():
    op.drop_table("report_subscribe_shift_association")
