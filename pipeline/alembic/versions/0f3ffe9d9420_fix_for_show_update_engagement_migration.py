"""fix for show/update engagement migration

Revision ID: 0f3ffe9d9420
Revises: 32a4cb053b94
Create Date: 2018-08-27 17:31:44.940703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f3ffe9d9420'
down_revision = '32a4cb053b94'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('warehouse', sa.Column('show_engagement', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('warehouse', sa.Column('update_engagement', sa.Boolean(), nullable=False, server_default=sa.true()))

def downgrade():
    op.drop_column('warehouse', 'show_engagement')
    op.drop_column('warehouse', 'update_engagement')
