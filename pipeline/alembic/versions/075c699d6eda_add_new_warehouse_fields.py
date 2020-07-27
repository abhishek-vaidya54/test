"""add_new_warehouse_fields

Revision ID: 075c699d6eda
Revises: c43f19996d44
Create Date: 2020-07-21 23:34:36.959806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "075c699d6eda"
down_revision = "c43f19996d44"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column("number_of_user_allocated", sa.Integer(), nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("city", sa.String(length=20), nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("state", sa.String(length=20), nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("country", sa.String(length=20), nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("industry", sa.String(length=20), nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("latitude", sa.Float, nullable=False),
    )
    op.add_column(
        "warehouse", sa.Column("longitude", sa.Float, nullable=False),
    )


def downgrade():
    op.drop_column("warehouse", "number_of_user_allocated")
    op.drop_column("warehouse", "city")
    op.drop_column("warehouse", "state")
    op.drop_column("warehouse", "country")
    op.drop_column("warehouse", "industry")
    op.drop_column("warehouse", "latitude")
    op.drop_column("warehouse", "longitude")

