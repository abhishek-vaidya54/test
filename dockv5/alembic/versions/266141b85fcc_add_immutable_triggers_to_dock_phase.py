"""add_immutable_triggers_to_dock_phase

Revision ID: 266141b85fcc
Revises: 32e967428b73
Create Date: 2019-11-25 16:30:23.349858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266141b85fcc'
down_revision = '32e967428b73'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # sql_trigger = "CREATE TRIGGER dock_phase_block_row_update BEFORE UPDATE ON dock_phase \
    #                 FOR EACH ROW\
    #                 BEGIN \
    #                     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You can not update dock_phase';\
    #                 END;"

    # op.execute(sql_trigger)
    # sql_trigger = "CREATE TRIGGER dock_phase_block_row_delete BEFORE DELETE ON dock_phase \
    #                 FOR EACH ROW\
    #                 BEGIN \
    #                     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You can not delete dock_phase';\
    #                 END;"

    # op.execute(sql_trigger)


def downgrade():
    pass
    # op.execute('DROP TRIGGER IF EXISTS dock_phase_block_row_update')
    # op.execute('DROP TRIGGER IF EXISTS dock_phase_block_row_delete')
