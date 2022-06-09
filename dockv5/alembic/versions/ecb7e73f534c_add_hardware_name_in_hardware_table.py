"""add_hardware_name_in_hardware_table

Revision ID: ecb7e73f534c
Revises: ee82a82ec5d1
Create Date: 2022-06-02 12:06:23.022022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ecb7e73f534c"
down_revision = "ee82a82ec5d1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "hardware",
        sa.Column("name", sa.String(length=90), nullable=True),
    )


def downgrade():
    op.drop_column("hardware", "name")
