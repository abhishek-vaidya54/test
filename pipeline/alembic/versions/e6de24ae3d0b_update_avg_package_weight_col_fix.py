"""update avg_package_weight col fix

Revision ID: e6de24ae3d0b
Revises: 7ede22264174
Create Date: 2018-12-14 15:10:30.967663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6de24ae3d0b'
down_revision = '7ede22264174'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('job_function', 'avg_package_weight', type_=sa.FLOAT(), default=6.6)
    op.execute('UPDATE job_function SET avg_package_weight = max_package_mass')


def downgrade():
    op.alter_column('job_function', 'avg_package_weight', type_=sa.INTEGER(), nullable=True)