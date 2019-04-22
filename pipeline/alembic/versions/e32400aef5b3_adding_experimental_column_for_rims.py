"""adding experimental column for rims

Revision ID: e32400aef5b3
Revises: f1b836de3a04
Create Date: 2019-03-21 17:11:55.574872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36ba8ab8d50'
down_revision = 'f1b836de3a04'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('client', sa.Column('experimental', sa.VARCHAR(length=45), nullable=True))

def downgrade():
    op.drop_column('client', 'experimental')