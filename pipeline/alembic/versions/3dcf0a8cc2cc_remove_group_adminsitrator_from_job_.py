"""Remove group adminsitrator from job functions

Revision ID: 3dcf0a8cc2cc
Revises: a8c2b9ed7d43
Create Date: 2021-12-15 18:01:26.254607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dcf0a8cc2cc'
down_revision = 'a8c2b9ed7d43'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('job_function', 'group_administrator')


def downgrade():
    op.add_column('job_function', sa.Column(
        'group_administrator', sa.String, nullable=True))
