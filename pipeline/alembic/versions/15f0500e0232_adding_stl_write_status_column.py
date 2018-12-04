"""adding stl write status column

Revision ID: 15f0500e0232
Revises: 4341fca459c2
Create Date: 2018-12-04 11:39:15.903306

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '15f0500e0232'
down_revision = '4341fca459c2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pipeline_events')
    op.add_column('processed_file', sa.Column('stl_write_status', sa.Unicode(length=45), nullable=True))


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

    op.drop_column('processed_file', 'stl_write_status')