"""Add Trained and Harness provided in imported Industrial Athletes

Revision ID: 2dec19f9f0f0
Revises: 4aabd584e0f5
Create Date: 2021-11-22 13:18:59.211850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dec19f9f0f0'
down_revision = '4aabd584e0f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("trained", sa.Boolean(), nullable=True, server_default="0"),
    )
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("harness_provided", sa.Boolean(),
                  nullable=True, server_default="0"),
    )


def downgrade():
    op.drop_column("imported_industrial_athlete", "trained")
    op.drop_column("imported_industrial_athlete", "harness_provided")
