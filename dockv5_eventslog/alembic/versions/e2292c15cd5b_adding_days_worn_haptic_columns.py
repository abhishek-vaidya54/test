"""adding days worn haptic columns

Revision ID: e2292c15cd5b
Revises: 2cda21e2d51a
Create Date: 2018-09-10 12:25:04.882774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e2292c15cd5b"
down_revision = "2cda21e2d51a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "engagement_stats",
        sa.Column(
            "days_worn_haptic_enabled", sa.Integer(), nullable=False, server_default="0"
        ),
    )
    op.add_column(
        "engagement_stats",
        sa.Column(
            "days_worn_haptic_disabled",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade():
    op.drop_column("engagement_stats", "days_worn_haptic_enabled")
    op.drop_column("engagement_stats", "days_worn_haptic_disabled")
