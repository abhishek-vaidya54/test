"""add client field customization

Revision ID: 55379c2e7cdc
Revises: f0daa37ace1f
Create Date: 2020-08-11 16:34:31.645711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55379c2e7cdc"
down_revision = "f0daa37ace1f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column("firstname_format", sa.String(length=20), server_default="capital"),
    )
    op.add_column(
        "client",
        sa.Column("lastname_format", sa.String(length=20), server_default="capital"),
    )


def downgrade():
    op.drop_column("client", "firstname_format")
    op.drop_column("client", "lastname_format")
