"""add_override_settings_to_job_functions

Revision ID: 093036ce8f92
Revises: 49b58ea545e2
Create Date: 2021-07-26 16:58:04.597567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "093036ce8f92"
down_revision = "49b58ea545e2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "job_function",
        sa.Column(
            "override_settings", sa.Boolean(), nullable=False, server_default="0"
        ),
    )


def downgrade():
    op.drop_column("job_function", "override_settings")
