"""dropping cols from monthly_safety

Revision ID: b9e3b9aa6929
Revises: 0a00a8fbd02e
Create Date: 2018-09-28 16:40:50.536443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9e3b9aa6929'
down_revision = '0a00a8fbd02e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('monthly_safety', 'safety_standard')
    op.drop_column('monthly_safety', 'status')
    op.drop_column('monthly_safety', 'color')

def downgrade():
    op.add_column('monthly_safety', sa.Column('safety_standard', sa.FLOAT(), nullable=False, server_default='0'))
    op.add_column('monthly_safety', sa.Column('status', sa.TEXT(), nullable=False, server_default=''))
    op.add_column('monthly_safety', sa.Column('color', sa.TEXT(), nullable=False, server_default=''))