"""add timezone to warehouse

Revision ID: 29941a2fcafd
Revises: 13d0b906054b
Create Date: 2021-02-18 12:28:15.928601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "29941a2fcafd"
down_revision = "13d0b906054b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "warehouse",
        sa.Column("timezone", sa.String(50), server_default="UTC", nullable=False),
    )


def downgrade():
    op.drop_column("warehouse", "timezone")
