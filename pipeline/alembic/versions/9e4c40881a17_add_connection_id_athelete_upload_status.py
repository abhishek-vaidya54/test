"""add connection_id athelete_upload_status

Revision ID: 9e4c40881a17
Revises: 37a01265c977
Create Date: 2020-08-15 15:41:34.782635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e4c40881a17"
down_revision = "37a01265c977"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "athlete_upload_status",
        sa.Column("connection_id", sa.String(length=30), nullable=True),
    )


def downgrade():
    op.drop_column("athlete_upload_status", "connection_id")
