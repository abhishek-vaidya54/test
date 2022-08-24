"""add_supervisor_id_in_imported_industrial_athletes

Revision ID: 8c094ff04dcd
Revises: efe288a7721b
Create Date: 2022-08-24 14:19:18.807365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c094ff04dcd"
down_revision = "efe288a7721b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("supervisor_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("imported_industrial_athlete", "supervisor_id")
