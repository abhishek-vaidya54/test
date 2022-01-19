"""update avg_package_weight col

Revision ID: 7ede22264174
Revises: 15f0500e0232
Create Date: 2018-12-14 14:24:12.170097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7ede22264174"
down_revision = "15f0500e0232"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("job_function", "avg_package_weight", type=sa.FLOAT(), default=6.6)
    op.execute("UPDATE job_function SET avg_package_weight = max_package_mass")


def downgrade():
    op.alter_column(
        "job_function", "avg_package_weight", type=sa.INTEGER(), nullable=True
    )
