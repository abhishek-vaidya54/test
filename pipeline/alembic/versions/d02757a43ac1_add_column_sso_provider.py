"""Add column sso_provider

Revision ID: d02757a43ac1
Revises: ac32b3b8ec9d
Create Date: 2021-03-16 13:26:51.086476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd02757a43ac1'
down_revision = 'ac32b3b8ec9d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column(
            "sso_provider",
            sa.String(length=45),
            nullable=True
        ),
    )
    op.execute('UPDATE client SET sso_provider = "okta" WHERE subdomain = "strongarm"')


def downgrade():
    op.drop_column("client", "sso_provider")
