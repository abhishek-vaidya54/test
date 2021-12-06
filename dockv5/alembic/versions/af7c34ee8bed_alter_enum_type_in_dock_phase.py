"""Alter_enum_type_in_dock_phase

Revision ID: af7c34ee8bed
Revises: a84e5071162a
Create Date: 2021-12-01 11:49:27.650835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af7c34ee8bed'
down_revision = 'a84e5071162a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE dock_phase MODIFY COLUMN phase enum('DEPLOYED','NOT DEPLOYED','MAINTENANCE', 'RETIRED')")


def downgrade():
    op.execute(
        "ALTER TABLE dock_phase MODIFY COLUMN phase enum('DEPLOYED','NOT DEPLOYED','MAINTENANCE')")
