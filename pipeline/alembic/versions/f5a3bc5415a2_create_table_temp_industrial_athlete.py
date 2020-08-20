"""create table temp_industrial_athlete

Revision ID: f5a3bc5415a2
Revises: 9e4c40881a17
Create Date: 2020-08-20 12:49:06.252007

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f5a3bc5415a2"
down_revision = "9e4c40881a17"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "temp_industrial_athlete",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("shift_id", sa.Integer(), nullable=False),
        sa.Column("job_function_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(length=1), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
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
    op.drop_table("temp_industrial_athlete")

