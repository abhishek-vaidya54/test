"""add_insert_trigger_to_config

Revision ID: 32e967428b73
Revises: 98fff9715050
Create Date: 2019-11-23 12:12:36.446379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32e967428b73'
down_revision = '98fff9715050'
branch_labels = None
depends_on = None


def upgrade():
    sql_trigger = "CREATE TRIGGER insert_dock_id_in_dock_phase AFTER INSERT ON config \
                    FOR EACH ROW\
                    BEGIN \
                        INSERT INTO dock_phase (dock_id,deployment_stage) VALUES (NEW.dock_id,NEW.deployment_stage);\
                    END;"

    op.execute(sql_trigger)


def downgrade():
    op.execute('DROP TRIGGER IF EXISTS insert_dock_id_in_dock_phase')
