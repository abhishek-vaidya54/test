"""create table bulk_upload_log

Revision ID: 68982e963b88
Revises: f5a3bc5415a2
Create Date: 2020-08-20 18:33:25.611295

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "68982e963b88"
down_revision = "f5a3bc5415a2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bulk_upload_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("count", sa.Integer(), nullable=True),
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
    op.drop_table("bulk_upload_log")
