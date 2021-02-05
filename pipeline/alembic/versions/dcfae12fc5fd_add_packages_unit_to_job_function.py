"""add_packages_unit_to_job_function

Revision ID: dcfae12fc5fd
Revises: 160984874ff3
Create Date: 2021-02-02 15:49:31.601900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dcfae12fc5fd"
down_revision = "160984874ff3"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "job_function",
        sa.Column(
            "package_unit", sa.Enum("KG", "LBS"), server_default="LBS", nullable=False
        ),
    )


def downgrade():
    op.drop_column("job_function", "package_unit")
