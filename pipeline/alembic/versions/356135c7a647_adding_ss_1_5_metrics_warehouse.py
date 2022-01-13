"""adding_SS_1.5_metrics_warehouse

Revision ID: 356135c7a647
Revises: 2efae14f67f9
Create Date: 2019-08-22 15:33:40.356809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "356135c7a647"
down_revision = "2efae14f67f9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("warehouse", sa.Column("standard_score", sa.Float, nullable=True))
    op.add_column("warehouse", sa.Column("min_safety_score", sa.Float, nullable=True))
    op.add_column("warehouse", sa.Column("max_safety_score", sa.Float, nullable=True))
    op.add_column(
        "warehouse", sa.Column("first_quarter_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "warehouse", sa.Column("median_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "warehouse", sa.Column("third_quarter_safety_score", sa.Float, nullable=True)
    )


def downgrade():
    op.drop_column("warehouse", "standard_score")
    op.drop_column("warehouse", "min_safety_score")
    op.drop_column("warehouse", "max_safety_score")
    op.drop_column("warehouse", "first_quarter_safety_score")
    op.drop_column("warehouse", "median_safety_score")
    op.drop_column("warehouse", "third_quarter_safety_score")
