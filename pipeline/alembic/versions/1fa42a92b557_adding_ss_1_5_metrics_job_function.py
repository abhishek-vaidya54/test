"""adding_ss_1_5_metrics_job_function

Revision ID: 1fa42a92b557
Revises: 356135c7a647
Create Date: 2019-08-22 15:47:42.541887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1fa42a92b557"
down_revision = "356135c7a647"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "job_function", sa.Column("min_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "job_function", sa.Column("max_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "job_function", sa.Column("first_quarter_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "job_function", sa.Column("median_safety_score", sa.Float, nullable=True)
    )
    op.add_column(
        "job_function", sa.Column("third_quarter_safety_score", sa.Float, nullable=True)
    )


def downgrade():
    op.drop_column("job_function", "min_safety_score")
    op.drop_column("job_function", "max_safety_score")
    op.drop_column("job_function", "first_quarter_safety_score")
    op.drop_column("job_function", "median_safety_score")
    op.drop_column("job_function", "third_quarter_safety_score")
