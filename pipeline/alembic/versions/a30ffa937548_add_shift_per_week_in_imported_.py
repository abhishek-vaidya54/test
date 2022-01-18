"""add_shift_per_week_in_imported_industrial_athlete

Revision ID: a30ffa937548
Revises: 589df1b771eb
Create Date: 2022-01-18 13:45:02.089594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a30ffa937548'
down_revision = '589df1b771eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('imported_industrial_athlete', sa.Column(
        'shift_per_week', sa.Integer, nullable=False, default=0))


def downgrade():
    op.drop_column('imported_industrial_athlete', 'shift_per_week')
