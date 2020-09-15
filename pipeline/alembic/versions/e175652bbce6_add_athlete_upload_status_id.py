"""add athlete_upload_status_id

Revision ID: e175652bbce6
Revises: b481cf862c87
Create Date: 2020-08-21 18:09:19.502570

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e175652bbce6"
down_revision = "b481cf862c87"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "imported_industrial_athlete",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "athlete_upload_status_id",
            sa.Integer(),
            sa.ForeignKey("athlete_upload_status.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("shift_id", sa.Integer(), nullable=False),
        sa.Column("job_function_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(length=1), nullable=True),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column(
            "hire_date", sa.DateTime, default=datetime.datetime.utcnow, nullable=False
        ),
        sa.Column("termination_date", sa.DateTime, nullable=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_updated_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("imported_industrial_athlete")

