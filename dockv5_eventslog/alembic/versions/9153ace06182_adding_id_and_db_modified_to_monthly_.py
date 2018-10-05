"""adding id and db_modified to monthly safety

Revision ID: 9153ace06182
Revises: b9e3b9aa6929
Create Date: 2018-10-04 11:36:28.002386

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '9153ace06182'
down_revision = 'b9e3b9aa6929'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('monthly_safety', sa.Column('id', sa.INTEGER(), primary_key= True, nullable=False, server_default='0'))
    op.add_column('monthly_safety', sa.Column('db_modified_at', sa.DATETIME(), nullable=False, onupdate= datetime.datetime.now))

def downgrade():

    op.drop_column('monthly_safety', 'id')
    op.drop_column('monthly_safety', 'db_modified_at')
