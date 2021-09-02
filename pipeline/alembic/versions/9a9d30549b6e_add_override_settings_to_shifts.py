"""add_override_settings_to_shifts

Revision ID: 9a9d30549b6e
Revises: 093036ce8f92
Create Date: 2021-07-26 16:59:20.941839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9a9d30549b6e"
down_revision = "093036ce8f92"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "shifts",
        sa.Column(
            "override_settings", sa.Boolean(), nullable=False, server_default="0"
        ),
    )


def downgrade():
    op.drop_column("shifts", "override_settings")
