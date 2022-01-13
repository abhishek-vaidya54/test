"""adding a event_hash field to check for event existence

Revision ID: 0a00a8fbd02e
Revises: e2292c15cd5b
Create Date: 2018-09-13 11:07:03.559292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0a00a8fbd02e"
down_revision = "e2292c15cd5b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "raw_event_log",
        sa.Column(
            "event_hash", sa.VARCHAR(length=40), nullable=False, server_default=""
        ),
    )


def downgrade():
    op.drop_column("raw_event_log", "event_hash")
