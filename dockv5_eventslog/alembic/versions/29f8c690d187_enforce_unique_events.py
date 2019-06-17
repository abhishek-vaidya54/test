"""enforce unique events

Revision ID: 29f8c690d187
Revises: d09c1e9e75d5
Create Date: 2019-06-13 15:55:00.968575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29f8c690d187'
down_revision = 'd09c1e9e75d5'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('raw_event_log', 'event_hash')
    op.execute('ALTER TABLE raw_event_log ADD COLUMN event_hash CHAR(32) GENERATED ALWAYS AS (md5(event_blob))')
    op.create_unique_constraint("event_hash_index", "raw_event_log", ["event_hash"])


def downgrade():
    op.drop_constraint("event_hash_index", "raw_event_log")
    op.drop_column('raw_event_log', 'event_hash')
    op.add_column('raw_event_log', sa.Column('event_hash', sa.VARCHAR(length=40), nullable=False, server_default=''))