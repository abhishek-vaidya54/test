"""Remove looker_user_id column from external_admin_user table

Revision ID: f4b3b0d140f2
Revises: d98541feeae3
Create Date: 2021-01-28 13:02:26.148215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f4b3b0d140f2"
down_revision = "d98541feeae3"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("external_admin_user", "looker_user_id")


def downgrade():
    op.add_column(
        "external_admin_user",
        sa.Column("looker_user_id", sa.Integer(), nullable=True, server_default="49"),
    )
