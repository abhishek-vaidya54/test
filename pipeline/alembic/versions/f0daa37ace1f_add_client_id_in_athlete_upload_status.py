"""add client_id in athlete_upload_status

Revision ID: f0daa37ace1f
Revises: cef17c523793
Create Date: 2020-08-11 15:21:03.659664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f0daa37ace1f"
down_revision = "cef17c523793"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "athlete_upload_status",
        sa.Column("client_id", sa.Integer(), nullable=False),
    )


def downgrade():
    op.drop_column("athlete_upload_status", "client_id")
