"""add_priority_to_rule_table

Revision ID: e9ffd78b0f92
Revises: e7ff0ada0d27
Create Date: 2019-04-04 00:14:17.421828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9ffd78b0f92'
down_revision = 'e7ff0ada0d27'
branch_labels = None
depends_on = None


def upgrade():
	op.add_column('rule', sa.Column('priority', sa.Integer(), nullable=True))
	pass


def downgrade():
	op.drop_column('rule', 'priority')
	pass
