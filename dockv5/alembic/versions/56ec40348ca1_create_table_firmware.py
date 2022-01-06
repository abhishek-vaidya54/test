"""create_table_firmware

Revision ID: 56ec40348ca1
Revises: 91afe9ca0df1
Create Date: 2021-12-27 12:47:40.425569

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56ec40348ca1'
down_revision = '91afe9ca0df1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "firmware",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column('hardware_id', sa.Integer(), nullable=False),
        sa.Column('device_type_id', sa.Integer(), nullable=False),
        sa.Column("version", sa.String(length=255), nullable=False),
        sa.Column("s3_url", sa.String(length=255), nullable=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ['hardware_id'], ['hardware.id'], name='fk_firmware_hardware'),
        sa.ForeignKeyConstraint(['device_type_id'], [
                                'device_type.id'], name='fk_firmware_device_type')
    )


def downgrade():
    op.drop_table("firmware")
