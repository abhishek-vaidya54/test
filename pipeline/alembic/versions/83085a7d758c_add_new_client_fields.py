"""add_new_client_fields

Revision ID: 83085a7d758c
Revises: f138c12cbbc5
Create Date: 2020-07-21 23:14:11.010115

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "83085a7d758c"
down_revision = "a869323a5477"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column("status", sa.String(length=20), nullable=False),
    )
    op.add_column(
        "client",
        sa.Column("contracted_users", sa.Integer(), nullable=False),
    )
    op.add_column(
        "client",
        sa.Column(
            "active_inactive_date",
            sa.DateTime,
            default=datetime.datetime.now(),
            # nullable=False,
        ),
    )


def downgrade():
    op.drop_column("client", "status")
    op.drop_column("client", "contracted_users")
    op.drop_column("client", "active_inactive_date")
