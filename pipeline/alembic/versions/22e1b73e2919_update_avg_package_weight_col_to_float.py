"""update avg_package_weight col to float

Revision ID: 22e1b73e2919
Revises: 4341fca459c2
Create Date: 2018-12-14 15:17:19.117932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22e1b73e2919'
down_revision = '4341fca459c2'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('job_function', 'avg_package_weight', type_=sa.FLOAT(), default=6.6)
    op.execute('UPDATE job_function SET avg_package_weight = max_package_mass')


def downgrade():
    op.alter_column('job_function', 'avg_package_weight', type_=sa.INTEGER(), nullable=True)