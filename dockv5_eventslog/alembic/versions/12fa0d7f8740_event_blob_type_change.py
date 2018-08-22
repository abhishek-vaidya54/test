"""event_blob type change

Revision ID: 12fa0d7f8740
Revises: 0c9d8014439e
Create Date: 2018-08-22 13:52:45.293709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12fa0d7f8740'
down_revision = '0c9d8014439e'
branch_labels = None
depends_on = None


def upgrade():
    # ALTER TABLE raw_event_log MODIFY COLUMN event_blob JSON;
    op.alter_column('raw_event_log','event_blob', type_=sa.Unicode(length=1000), existing_server_default=False, existing_nullable=True)
    op.alter_column('raw_event_log','event_blob', type_=sa.JSON(), existing_server_default=False, existing_nullable=True)


def downgrade():
    op.alter_column('raw_event_log','event_blob', type_=sa.BLOB(), existing_server_default=False, existing_nullable=True)