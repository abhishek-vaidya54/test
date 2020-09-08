"""add_ex_admin_role_field

Revision ID: a0ee75053872
Revises: 3c18799b7513
Create Date: 2020-07-30 13:17:43.976327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0ee75053872"
down_revision = "3c18799b7513"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "external_admin_user", sa.Column("role", sa.String(length=20), nullable=True),
    )


def downgrade():
    op.drop_column("external_admin_user", "role")
