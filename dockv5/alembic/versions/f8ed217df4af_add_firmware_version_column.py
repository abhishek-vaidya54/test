"""add firmware version column

Revision ID: f8ed217df4af
Revises: 3bb7f41f39e8
Create Date: 2019-01-11 11:04:49.987649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8ed217df4af"
down_revision = "3bb7f41f39e8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("config", sa.Column("firmware_version", sa.Integer, nullable=True))


def downgrade():
    op.drop_column("config", "firmware_version")
