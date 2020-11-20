"""add is_active in exetrnal_admin_user

Revision ID: 0e25b3d033ee
Revises: d9d26752ef2b
Create Date: 2020-09-15 15:24:02.393397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0e25b3d033ee"
down_revision = "d9d26752ef2b"
branch_labels = None
depends_on = None


def upgrade():
    print("Skipping")
    # op.add_column(
    #     "external_admin_user",
    #     sa.Column("is_active", sa.String(length=5), server_default="true"),
    # )


def downgrade():
    op.drop_column("external_admin_user", "is_active")
