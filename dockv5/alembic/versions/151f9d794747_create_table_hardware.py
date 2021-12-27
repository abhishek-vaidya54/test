"""create_table_hardware

Revision ID: 151f9d794747
Revises: af7c34ee8bed
Create Date: 2021-12-27 12:33:11.976032

"""
import datetime
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '151f9d794747'
down_revision = 'af7c34ee8bed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "hardware",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(length=255), nullable=False),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("hardware")
