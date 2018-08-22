"""adding standard score column to job function table

Revision ID: 04c7704cf10a
Revises: 2b79467ba0d8
Create Date: 2018-07-16 18:22:59.360862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04c7704cf10a'
down_revision = '2b79467ba0d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('warehouse', sa.Column('show_engagement', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('warehouse', sa.Column('update_engagement', sa.Boolean(), nullable=False, server_default=sa.true()))

def downgrade():
    op.drop_column('warehouse', 'show_engagement')
    op.drop_column('warehouse', 'update_engagement')
