"""delete athlete_upload_status_id

Revision ID: b481cf862c87
Revises: 68982e963b88
Create Date: 2020-08-21 18:09:06.629114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b481cf862c87"
down_revision = "68982e963b88"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("imported_industrial_athlete")


def downgrade():
    pass

