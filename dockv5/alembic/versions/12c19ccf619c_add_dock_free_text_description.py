"""Add dock free text description

Revision ID: 12c19ccf619c
Revises: f8ed217df4af
Create Date: 2019-06-18 12:08:46.793390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "12c19ccf619c"
down_revision = "f8ed217df4af"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("config", sa.Column("description", sa.VARCHAR(500)))


def downgrade():
    op.drop_column("config", "description")
