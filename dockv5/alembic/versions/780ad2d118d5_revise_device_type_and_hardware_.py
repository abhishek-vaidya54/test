"""Revise device type and hardware structure

Revision ID: 780ad2d118d5
Revises: f5da1c70f358
Create Date: 2022-06-08 13:13:08.188145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "780ad2d118d5"
down_revision = "f5da1c70f358"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("fk_firmware_device_type", "firmware", "foreignkey")
    op.drop_column("firmware", "device_type_id")
    op.add_column("hardware", sa.Column("device_type_id", sa.Integer, nullable=True))
    op.create_foreign_key(
        "fk_hardware_device_type",
        "hardware",
        "device_type",
        ["device_type_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("fk_hardware_device_type", "hardware", "foreignkey")
    op.drop_column("hardware", "device_type_id")
    op.add_column("firmware", sa.Column("device_type_id", sa.Integer, nullable=True))
    op.create_foreign_key(
        "fk_firmware_device_type",
        "firmware",
        "device_type",
        ["device_type_id"],
        ["id"],
    )
