"""alter_target_type

Revision ID: aecb939b58d0
Revises: 9a9d30549b6e
Create Date: 2021-07-26 17:11:14.339324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aecb939b58d0"
down_revision = "9a9d30549b6e"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("settings", "target_type")
    op.add_column(
        "settings",
        sa.Column(
            "target_type",
            sa.Enum(
                "group",
                "warehouse",
                "jobfunction",
                "industrial_athlete",
                "shift",
            ),
            server_default="group",
        ),
    )


def downgrade():
    op.drop_column("settings", "target_type")
    op.add_column(
        "settings",
        sa.Column("target_type", sa.String(length=255), nullable=False),
    )
