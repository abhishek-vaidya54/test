"""create_rule_table

Revision ID: aad3c8a056c6
Revises: 08101dc26550
Create Date: 2019-02-21 12:18:14.593817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad3c8a056c6'
down_revision = '08101dc26550'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('rule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('params', sa.String(length=1024), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='1'),
				sa.Column('deleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('db_created_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ), 
        sa.Column('db_updated_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('rule')
