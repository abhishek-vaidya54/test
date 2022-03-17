"""add_batch_number_athlete_upload_status

Revision ID: 60004256e42a
Revises: ccb6bc751210
Create Date: 2022-03-16 17:26:50.188305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60004256e42a'
down_revision = 'ccb6bc751210'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "athlete_upload_status",
        sa.Column("batch", sa.Integer, nullable=False, default=0),
    )


def downgrade():
    op.drop_column("athlete_upload_status", "batch")
