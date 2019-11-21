"""change_dock_phase_timestamp_from_datetime_to_timestamp

Revision ID: 98fff9715050
Revises: 4005f9a0e44c
Create Date: 2019-11-21 17:24:35.770752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '98fff9715050'
down_revision = '4005f9a0e44c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('dock_phase', 'timestamp', existing_type=sa.DateTime,type_=sa.TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))


def downgrade():
    op.alter_column('dock_phase', 'timestamp', existing_type=sa.TIMESTAMP,type_=sa.DateTime,server_default=text('CURRENT_TIMESTAMP'))