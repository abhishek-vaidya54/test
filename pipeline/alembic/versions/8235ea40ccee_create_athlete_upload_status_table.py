"""create_athlete_upload_status_table

Revision ID: 8235ea40ccee
Revises: a0ee75053872
Create Date: 2020-08-10 16:05:12.702341

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "8235ea40ccee"
down_revision = "a0ee75053872"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "athlete_upload_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("processed", sa.Integer(), nullable=False, default=0),
        sa.Column("total", sa.Integer(), nullable=False, default=0),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.Column(
            "db_updated_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("athlete_upload_status")
