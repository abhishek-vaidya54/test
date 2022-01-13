"""on update_trigger

Revision ID: eb8099f52707
Revises: 38886a28cf02
Create Date: 2019-09-12 15:00:59.780075

"""
from alembic import op
import sqlalchemy as sa

# updating trigger

# revision identifiers, used by Alembic.
revision = "eb8099f52707"
down_revision = "38886a28cf02"
branch_labels = None
depends_on = None


def upgrade():
    sql_trigger = "CREATE TRIGGER update_dock_phase_deployment_stage AFTER UPDATE ON config \
                    FOR EACH ROW\
                    BEGIN \
                    DECLARE phase_ VARCHAR(45);\
                        IF (OLD.deployment_stage != NEW.deployment_stage) THEN\
                            SELECT phase INTO phase_ FROM dock_phase WHERE dock_phase.phase IS NOT NULL AND dock_phase.dock_id = OLD.dock_id ORDER BY dock_phase.timestamp DESC LIMIT 1;\
                            INSERT INTO dock_phase (dock_id,phase,deployment_stage) VALUES (OLD.dock_id,phase_,NEW.deployment_stage);\
                        END IF;\
                    END;"

    op.execute(sql_trigger)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS update_dock_phase_deployment_stage")
