"""adding two tables for data-funnel tracking

Revision ID: 32a4cb053b94
Revises: 04c7704cf10a
Create Date: 2018-08-13 17:52:57.464406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32a4cb053b94'
down_revision = '04c7704cf10a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('binary_bucket_monitor',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(length=50), nullable=True),
    sa.Column('athlete_id', sa.String(length=50), nullable=True),
    sa.Column('dock_id', sa.String(length=50), nullable=True),
    sa.Column('client_id', sa.String(length=50), nullable=True),
    sa.Column('warehouse_id', sa.String(length=50), nullable=True),
    sa.Column('firmware_version', sa.String(length=50), nullable=True),
    sa.Column('assignment_time', sa.String(length=50), nullable=True),
    sa.Column('session_id', sa.String(length=50), nullable=False),
    sa.Column('db_created_at', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
    sa.Column('db_modified_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
    sa.Column('file_size', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )

    op.create_table('parser_monitor',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(length=50), nullable=True),
    sa.Column('athlete_id', sa.String(length=50), nullable=True),
    sa.Column('dock_id', sa.String(length=50), nullable=True),
    sa.Column('client_id', sa.String(length=50), nullable=True),
    sa.Column('warehouse_id', sa.String(length=50), nullable=True),
    sa.Column('firmware_version', sa.String(length=50), nullable=True),
    sa.Column('assignment_time', sa.String(length=50), nullable=True),
    sa.Column('session_id', sa.String(length=50), nullable=False),
    sa.Column('db_created_at', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
    sa.Column('db_modified_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
    sa.Column('file_status', sa.String(length=50), nullable=False, server_default='parsing'),
    sa.Column('message', sa.String(length=50), nullable=False),
    sa.Column('file_size', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )

def downgrade():
    op.drop_table('binary_bucket_monitor')
    op.drop_table('parser_monitor')
