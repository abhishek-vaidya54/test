"""create_table_firmware_group_association

Revision ID: 5bd969cdbdd7
Revises: 82b2ed376947
Create Date: 2021-12-27 13:31:19.234594

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "5bd969cdbdd7"
down_revision = "82b2ed376947"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "firmware_group_association",
        sa.Column("firmware_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("firmware_group_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_modified_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        # sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["firmware_id"], ["firmware.id"], name="fk_firmware_group_assoc_firmware"
        ),
        sa.ForeignKeyConstraint(
            ["firmware_group_id"],
            ["firmware_group.id"],
            name="fk_firmware_group_assoc_firmware_group",
        ),
    )


def downgrade():
    op.drop_table("firmware_group_association")
