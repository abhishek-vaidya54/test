"""create external_id and warehouse_id index in industrial_athlete

Revision ID: f2d0e56105a8
Revises: 7a120d5585f5
Create Date: 2020-10-06 18:54:28.570868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f2d0e56105a8"
down_revision = "311422447dcb"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE industrial_athlete ADD UNIQUE (external_id, warehouse_id, termination_date);")


def downgrade():
    op.execute("DROP INDEX `external_id` ON industrial_athlete")