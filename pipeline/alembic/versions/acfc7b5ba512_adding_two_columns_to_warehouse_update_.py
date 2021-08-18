"""adding two columns to warehouse, update/show engagement

Revision ID: acfc7b5ba512
Revises: 393a95e87672
Create Date: 2018-08-22 17:10:29.610823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "acfc7b5ba512"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column(
            "show_engagement", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )
    op.add_column(
        "warehouse",
        sa.Column(
            "update_engagement", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
    )


def downgrade():
    op.drop_column("warehouse", "show_engagement")
    op.drop_column("warehouse", "update_engagement")
