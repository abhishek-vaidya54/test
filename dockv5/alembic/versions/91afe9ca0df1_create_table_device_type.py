"""create_table_device_type

Revision ID: 91afe9ca0df1
Revises: 151f9d794747
Create Date: 2021-12-27 12:45:14.358934

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '91afe9ca0df1'
down_revision = '151f9d794747'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "device_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("device_type")
