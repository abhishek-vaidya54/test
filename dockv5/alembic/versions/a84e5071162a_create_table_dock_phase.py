"""create table dock_phase

Revision ID: a84e5071162a
Revises: 97618bd2ecc2
Create Date: 2020-08-26 14:33:09.639953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "a84e5071162a"
down_revision = "97618bd2ecc2"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("dock_phase")
    op.create_table(
        "dock_phase",
        sa.Column(
            "id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("dock_id", sa.String(45), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("dock_firmware", sa.Boolean(), nullable=True, default=False),
        sa.Column("dock_firmware_version", sa.String(10), default=False),
        sa.Column("timestamp", sa.DateTime, server_default=text("CURRENT_TIMESTAMP()")),
        sa.Column(
            "phase",
            sa.Enum("DEPLOYED", "NOT DEPLOYED", "MAINTENANCE"),
            nullable=False,
            default="NOT DEPLOYED",
        ),
        sa.Column("phase_date", sa.DateTime, nullable=True),
        sa.Column(
            "deployment_stage", sa.Enum("DEV", "PROD"), nullable=False, default="dev"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass
