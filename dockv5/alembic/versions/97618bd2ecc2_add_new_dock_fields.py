"""add_new_dock_fields

Revision ID: 97618bd2ecc2
Revises: 266141b85fcc
Create Date: 2020-07-24 12:23:46.987541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97618bd2ecc2"
down_revision = "266141b85fcc"
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.add_column(
    #     "dock_phase",
    #     sa.Column(
    #         "client_id",
    #         sa.Integer(),
    #         sa.ForeignKey("pipeline.client.id"),
    #         nullable=True,
    #     ),
    # )
    # op.add_column(
    #     "dock_phase",
    #     sa.Column(
    #         "warehouse_id",
    #         sa.Integer(),
    #         sa.ForeignKey("pipeline.warehouse.id"),
    #         nullable=True,
    #     ),
    # )
    # op.add_column(
    #     "dock_phase", sa.Column("phase_date", sa.DateTime, nullable=True),
    # )
    # op.add_column(
    #     "dock_phase",
    #     sa.Column("dock_firmware_version", sa.String(length=10), nullable=False),
    # )
    # op.add_column(
    #     "dock_phase", sa.Column("description", sa.String(length=255), nullable=True),
    # )
    # op.add_column(
    #     "dock_phase",
    #     sa.Column("dock_firmware", sa.Boolean(), nullable=True, default=False),
    # )


def downgrade():
    pass
    # op.drop_column("dock_phase", "client_id")
    # op.drop_column("dock_phase", "warehouse_id")
    # op.drop_column("dock_phase", "phase_date")
    # op.drop_column("dock_phase", "dock_firmware_version")
    # op.drop_column("dock_phase", "description")
