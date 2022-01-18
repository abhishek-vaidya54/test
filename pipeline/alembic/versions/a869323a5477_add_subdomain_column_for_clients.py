"""add subdomain column for clients

Revision ID: a869323a5477
Revises: f138c12cbbc5
Create Date: 2020-07-17 19:54:12.262957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a869323a5477"
down_revision = "f138c12cbbc5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client", sa.Column("subdomain", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("client", "subdomain")
