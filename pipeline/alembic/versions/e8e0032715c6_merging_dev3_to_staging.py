"""merging dev3 to staging

Revision ID: e8e0032715c6
Revises: 49b58ea545e2, 0257cc2ab18c
Create Date: 2021-08-19 01:44:48.005758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e8e0032715c6"
down_revision = ("49b58ea545e2", "0257cc2ab18c")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
