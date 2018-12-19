"""drop pipeline events table

Revision ID: 4758c8be67c7
Revises: e6de24ae3d0b
Create Date: 2018-12-19 11:15:42.419828

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4758c8be67c7'
down_revision = 'e6de24ae3d0b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pipeline_events')

def downgrade():
    op.create_table('pipeline_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=255), nullable=False),
        sa.Column('state', sa.String(length=255), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('db_created_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ), 
        sa.PrimaryKeyConstraint('id')
    )