"""create sensors table

Revision ID: 7a120d5585f5
Revises: b0d0b3c39ada
Create Date: 2020-09-28 16:49:24.093418

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a120d5585f5"
down_revision = "b0d0b3c39ada"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sensors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("serial_number", sa.String(length=45), nullable=False),
        sa.Column("sensor_id", sa.String(length=45), nullable=True),
        sa.Column("stiction_flagged", sa.String(length=1), server_default="0", nullable=False),
        sa.Column("decommissioned", sa.String(length=1), server_default="0", nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("sensors")
