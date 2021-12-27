"""create_table_firmware_group

Revision ID: 82b2ed376947
Revises: 56ec40348ca1
Create Date: 2021-12-27 12:54:37.034208

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82b2ed376947'
down_revision = '56ec40348ca1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "firmware_group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("firmware_group")
