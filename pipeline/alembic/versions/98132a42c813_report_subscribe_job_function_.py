"""report_subscribe_job_function_association

Revision ID: 98132a42c813
Revises: 86bde3c0d58d
Create Date: 2022-05-30 17:24:51.767897

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "98132a42c813"
down_revision = "86bde3c0d58d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "report_subscribe_job_function_association",
        sa.Column(
            "report_subscribe_id", sa.Integer(), nullable=False, primary_key=True
        ),
        sa.Column("job_function_id", sa.Integer(), nullable=False, primary_key=True),
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
            name="fk_report_jobfunc_assoc_report_subscribe",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["job_function_id"],
            ["job_function.id"],
            name="fk_report_jobfunc_assoc_job_function",
            ondelete="CASCADE",
        ),
    )


def downgrade():
    op.drop_table("report_subscribe_job_function_association")
