"""add index to dockv5_events.sensor_events.type

Revision ID: e761d90139c6
Revises: 29f8c690d187
Create Date: 2020-07-21 09:40:56.946842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e761d90139c6'
down_revision = '29f8c690d187'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_type', 'sensor_events', ['type'])


def downgrade():
    op.drop_index('idx_type', 'sensor_events')
