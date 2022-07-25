"""add_supervisor_fields_in_external_admin_user

Revision ID: ed17a3e6fce9
Revises: 170232295d4f
Create Date: 2022-07-25 15:22:01.135615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ed17a3e6fce9"
down_revision = "170232295d4f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "external_admin_user",
        sa.Column("first_name", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "external_admin_user",
        sa.Column("last_name", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "external_admin_user",
        sa.Column("is_supervisor", sa.Boolean(), nullable=True, server_default="0"),
    )


def downgrade():
    op.drop_column("external_admin_user", "first_name")
    op.drop_column("external_admin_user", "last_name")
    op.drop_column("external_admin_user", "is_supervisor")
