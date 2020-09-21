"""add client name_format column

Revision ID: b38403920c58
Revises: ace2c9349ddf
Create Date: 2020-08-31 12:46:45.234513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b38403920c58"
down_revision = "ace2c9349ddf"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("client", "firstname_format")
    op.drop_column("client", "lastname_format")
    op.add_column(
        "client",
        sa.Column(
            "ia_name_format",
            sa.String(length=45),
            nullable=True,
            server_default="ANONYMOUS",
        ),
    )


def downgrade():
    op.add_column(
        "client",
        sa.Column("firstname_format", sa.String(length=20), server_default="capital"),
    )
    op.add_column(
        "client",
        sa.Column("lastname_format", sa.String(length=20), server_default="capital"),
    )
    op.drop_column("client", "ia_name_format")
