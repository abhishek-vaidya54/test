"""add_firmware_group_id_in_config_model

Revision ID: 2abfa9ce5b38
Revises: 5bd969cdbdd7
Create Date: 2021-12-27 16:06:31.049192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2abfa9ce5b38'
down_revision = '5bd969cdbdd7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('config', sa.Column(
        'firmware_group_id', sa.Integer, nullable=True))
    op.create_foreign_key(
        "fk_config_firmware_group",
        "config", "firmware_group",
        ["firmware_group_id"], ["id"])


def downgrade():
    op.drop_constraint("fk_config_firmware_group", "config", "foreignkey")
    op.drop_column('config', 'firmware_group_id')
