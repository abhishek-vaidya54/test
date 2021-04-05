"""remove timezone from shifts

Revision ID: d9c22c2126c3
Revises: 29941a2fcafd
Create Date: 2021-02-18 13:13:33.506621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d9c22c2126c3"
down_revision = "29941a2fcafd"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("shifts", "timezone")


def downgrade():
    op.add_column("shifts", sa.Column("timezone", sa.String(30), nullable=False))
