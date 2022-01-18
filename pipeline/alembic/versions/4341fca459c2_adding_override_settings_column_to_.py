"""adding override settings column to groups table

Revision ID: 4341fca459c2
Revises: b4fdb59eb515
Create Date: 2018-11-28 12:46:10.852608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4341fca459c2"
down_revision = "b4fdb59eb515"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "groups",
        sa.Column(
            "override_settings", sa.Boolean(), nullable=False, server_default="0"
        ),
    )


def downgrade():
    op.drop_column("groups", "override_settings")
