"""added_warehouse_id

Revision ID: b2688d95a8a9
Revises: 708aad9cd7f7
Create Date: 2020-07-21 12:29:11.330696

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, ForeignKey


# revision identifiers, used by Alembic.
revision = 'b2688d95a8a9'
down_revision = '708aad9cd7f7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dock_phase', Column('client_id', INTEGER, ForeignKey('client.id')))


def downgrade():
    op.drop_column('dock_phase', 'client_id')
