"""added_foreignkey_warehouse_id

Revision ID: 08ffe731e043
Revises: b2688d95a8a9
Create Date: 2020-07-21 12:31:59.037515

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, ForeignKey


# revision identifiers, used by Alembic.
revision = '08ffe731e043'
down_revision = 'b2688d95a8a9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dock_phase', Column('warehouse_id', INTEGER, ForeignKey('warehouse.id')))


def downgrade():
    op.drop_column('dock_phase', 'warehouse_id')
