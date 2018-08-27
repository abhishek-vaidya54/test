"""drop columns from raw events and add to keepalives

Revision ID: 2cda21e2d51a
Revises: 12fa0d7f8740
Create Date: 2018-08-24 11:13:47.954237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cda21e2d51a'
down_revision = '12fa0d7f8740'
branch_labels = None
depends_on = None


def upgrade():
    # add a bunch of columns to keepalive table to track new info
    op.add_column('keepalive_events', sa.Column('dockIMEI', sa.Unicode(length=45), nullable=True))
    op.add_column('keepalive_events', sa.Column('enum_ports', sa.Unicode(length=100), nullable=True))
    op.add_column('keepalive_events', sa.Column('occupied_ports', sa.Unicode(length=100), nullable=True))
    op.add_column('keepalive_events', sa.Column('local_sensor_fw', sa.Integer(), nullable=True))
    op.add_column('keepalive_events', sa.Column('app_version', sa.Unicode(length=45), nullable=True))

    # drop a bunch of columns from the raw_event_log
    op.drop_column('raw_event_log', 'timestamp')
    op.drop_column('raw_event_log', 'assignment_time')
    op.drop_column('raw_event_log', 'clientID')
    op.drop_column('raw_event_log', 'warehouseID')
    op.drop_column('raw_event_log', 'sensorID')
    op.drop_column('raw_event_log', 'athleteID')
    op.drop_column('raw_event_log', 'datarecord_count')
    op.drop_column('raw_event_log', 'port')
    op.drop_column('raw_event_log', 'firmware_version')
    op.drop_column('raw_event_log', 'survey_type')
    op.drop_column('raw_event_log', 'response')
    op.drop_column('raw_event_log', 'filename')
    op.drop_column('raw_event_log', 'batt_percent')
    op.drop_column('raw_event_log', 'charge_status')
    op.drop_column('raw_event_log', 'sessionID')

def downgrade():
    # drop a bunch of columns to keepalive table that track new info
    op.drop_column('keepalive_events', 'dockIMEI')
    op.drop_column('keepalive_events', 'enum_ports')
    op.drop_column('keepalive_events', 'occupied_ports')
    op.drop_column('keepalive_events', 'local_sensor_fw')
    op.drop_column('keepalive_events', 'app_version')

    # add a bunch of columns to the raw_event_log
    op.add_column('raw_event_log', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('raw_event_log', sa.Column('assignment_time', sa.Integer(), nullable=True))
    op.add_column('raw_event_log', sa.Column('clientID', sa.Unicode(length=50), nullable=True))
    op.add_column('raw_event_log', sa.Column('warehouseID', sa.Unicode(length=50), nullable=True))
    op.add_column('raw_event_log', sa.Column('sensorID', sa.Unicode(length=50), nullable=True))
    op.add_column('raw_event_log', sa.Column('athleteID', sa.Unicode(length=50), nullable=True))
    op.add_column('raw_event_log', sa.Column('datarecord_count', sa.Integer(), nullable=True))
    op.add_column('raw_event_log', sa.Column('port', sa.Integer(), nullable=True))
    op.add_column('raw_event_log', sa.Column('firmware_version', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('survey_type', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('response', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('filename', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('batt_percent', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('charge_status', sa.Unicode(length=45), nullable=True))
    op.add_column('raw_event_log', sa.Column('sessionID', sa.Unicode(length=45), nullable=True))