"""adding sensors table

Revision ID: f138c12cbbc5
Revises: ae41b9b137af
Create Date: 2020-07-10 11:49:53.227415

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = 'f138c12cbbc5'
down_revision = 'ae41b9b137af'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('sensors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('serial_number', sa.VARCHAR(length=45), nullable=False),
        sa.Column('sensor_id', sa.VARCHAR(length=45), nullable=True, default=None ),
        sa.Column('stiction_flagged', sa.VARCHAR(length=45), nullable=False, server_default='0'),
        sa.Column('decommissioned', sa.VARCHAR(length=45), nullable=False, server_default='0'),
        sa.Column('db_created_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ),
        sa.Column('db_modified_at', sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('sensors')