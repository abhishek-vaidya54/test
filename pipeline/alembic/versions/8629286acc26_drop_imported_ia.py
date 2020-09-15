"""drop imported_ia

Revision ID: 8629286acc26
Revises: 4000b95a31a2
Create Date: 2020-08-10 19:14:07.119189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8629286acc26'
down_revision = '4000b95a31a2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('imported_industrial_athlete')


def downgrade():
    pass
