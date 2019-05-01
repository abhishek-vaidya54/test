"""add_program_table

Revision ID: 423f4e59eb62
Revises: e9ffd78b0f92
Create Date: 2019-05-01 00:06:13.518456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '423f4e59eb62'
down_revision = 'e9ffd78b0f92'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('program',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
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
    op.drop_table('program')
