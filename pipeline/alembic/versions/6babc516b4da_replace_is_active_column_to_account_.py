"""Replace is_active column to account_status

Revision ID: 6babc516b4da
Revises: f5641c61905a
Create Date: 2021-06-28 17:05:57.375146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6babc516b4da'
down_revision = 'f5641c61905a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("external_admin_user", "is_active")
    op.add_column(
        "external_admin_user", sa.Column("account_status", sa.String(length=255), nullable=False, server_default='inactive')
    )


def downgrade():
    op.drop_column("external_admin_user", "account_status")
    op.add_column(
        "external_admin_user", sa.Column("is_active", sa.String(length=5), nullable=False, server_default='true')
    )
    
