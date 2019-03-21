"""create_condition_table

Revision ID: f1b836de3a04
Revises: aad3c8a056c6
Create Date: 2019-02-21 13:28:37.350994

"""
from alembic import op
import sqlalchemy as sa
import datetime



# revision identifiers, used by Alembic.
revision = 'f1b836de3a04'
down_revision = 'aad3c8a056c6'
branch_labels = None
depends_on = None


def upgrade():
		op.create_table('condition',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(length=255), nullable=False),
        sa.Column('operator', sa.String(length=255), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=False),
        sa.Column('rule_id', sa.Integer(), nullable=False),
        sa.Column('deleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('db_created_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ),
        sa.Column('db_updated_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ),
        sa.ForeignKeyConstraint(['rule_id'], ['rule.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('condition')
