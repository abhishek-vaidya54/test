"""add_trained_and_harness_provided_in_athlete_table

Revision ID: 2cdbc1d28383
Revises: 6694ad6868ed
Create Date: 2021-10-04 16:37:49.311640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2cdbc1d28383"
down_revision = "6694ad6868ed"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "industrial_athlete",
        sa.Column("trained", sa.Boolean(), nullable=True, server_default="0"),
    )
    op.add_column(
        "industrial_athlete",
        sa.Column("harness_provided", sa.Boolean(), nullable=True, server_default="0"),
    )


def downgrade():
    op.drop_column("industrial_athlete", "trained")
    op.drop_column("industrial_athlete", "harness_provided")
