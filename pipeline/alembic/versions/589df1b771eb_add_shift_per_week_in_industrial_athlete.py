"""add_shift_per_week_in_industrial_athlete

Revision ID: 589df1b771eb
Revises: 3fd026717c02
Create Date: 2022-01-18 13:44:53.717623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '589df1b771eb'
down_revision = '3fd026717c02'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('industrial_athlete', sa.Column(
        'shift_per_week', sa.Integer, nullable=False, default=0))


def downgrade():
    op.drop_column('industrial_athlete', 'shift_per_week')
