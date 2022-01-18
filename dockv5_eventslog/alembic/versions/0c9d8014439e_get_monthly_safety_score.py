"""get monthly safety score

Revision ID: 0c9d8014439e
Revises: 5457e3afe2d3
Create Date: 2018-07-18 13:15:39.017296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0c9d8014439e"
down_revision = "5457e3afe2d3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "monthly_safety",
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("latest_safety_score", sa.Float(), nullable=False),
        sa.Column("monthly_score", sa.Float(), nullable=True),
        sa.Column("safety_standard", sa.Float(), nullable=False, default=70),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("color", sa.Text(), nullable=False, default="#0CB074"),
        sa.PrimaryKeyConstraint("athlete_id"),
    )


def downgrade():
    op.drop_table("monthly_safety")
