"""remove warehouse_id and role from external_admin_user

Revision ID: 0dfec63dee9c
Revises: 7362f276939c
Create Date: 2021-01-20 13:31:11.632142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0dfec63dee9c"
down_revision = "7362f276939c"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("external_admin_user", "warehouse_id")
    op.drop_column("external_admin_user", "role")


def downgrade():
    op.add_column(
        "external_admin_user", sa.Column("warehouse_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "external_admin_user", sa.Column("role", sa.String(length=20), nullable=False)
    )
