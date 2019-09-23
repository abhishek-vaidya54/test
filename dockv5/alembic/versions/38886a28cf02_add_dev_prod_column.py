"""add_dev_prod_column

Revision ID: 38886a28cf02
Revises: ed9a52b2c17b
Create Date: 2019-09-12 14:15:06.996667

"""
from alembic import op
import sqlalchemy as sa

#adding columns to config table
# revision identifiers, used by Alembic.
revision = '38886a28cf02'
down_revision = '202c1e7a4440'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dock_phase',sa.Column('deployment_stage',sa.Enum('DEV','PROD'),server_default='DEV',nullable=False))


def downgrade():
    op.drop_column('dock_phase','deployment_stage')
