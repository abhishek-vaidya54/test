"""create_imported_industrial_athletes

Revision ID: 8c018c9c1cf7
Revises: 8235ea40ccee
Create Date: 2020-08-10 16:10:46.331705

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "8c018c9c1cf7"
down_revision = "8235ea40ccee"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "imported_industrial_athlete",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "athlete_upload_status_id",
            sa.Integer(),
            sa.ForeignKey("athlete_upload_status.id"),
            nullable=False,
        ),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("shift_id", sa.Integer(), nullable=False),
        sa.Column("job_function_id", sa.Integer(), nullable=False),
        sa.Column("setting_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("gender", sa.String(length=1), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("schedule", sa.String(length=255), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("prior_back_injuries", sa.String(length=255), nullable=True),
        sa.Column(
            "hire_date", sa.DateTime, default=datetime.datetime.utcnow, nullable=True
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
