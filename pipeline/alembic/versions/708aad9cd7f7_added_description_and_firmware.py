"""added_description_and_firmware

Revision ID: 708aad9cd7f7
Revises: ae41b9b137af
Create Date: 2020-07-21 12:20:30.214572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, ForeignKey

# revision identifiers, used by Alembic.
revision = '708aad9cd7f7'
down_revision = 'ae41b9b137af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dock_phase', sa.Column('dock_firmware', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('dock_phase', sa.Column('description', sa.VARCHAR(length=45), nullable=True))



def downgrade():
    op.drop_column('dock_phase', 'dock_firmware')
    op.drop_column('dock_phase', 'description')
