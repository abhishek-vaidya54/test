"""pipeline events table

Revision ID: b4fdb59eb515
Revises: aa5e10e70123
Create Date: 2018-11-26 13:08:15.906477

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "b4fdb59eb515"
down_revision = "aa5e10e70123"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pipeline_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=255), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column(
            "db_created_at",
            sa.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("pipeline_events")
