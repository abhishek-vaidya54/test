"""adding hide_judegement column in warehouse

Revision ID: 606fd41dcb5d
Revises: 63e6ca2dc249
Create Date: 2018-09-28 16:57:08.081756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '606fd41dcb5d'
down_revision = '63e6ca2dc249'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('warehouse', sa.Column('hide_judgement', sa.Boolean(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('warehouse', 'hide_judgement')

