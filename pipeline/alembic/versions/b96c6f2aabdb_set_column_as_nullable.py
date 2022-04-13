"""set column as nullable

Revision ID: b96c6f2aabdb
Revises: 85b346bbd89e
Create Date: 2022-04-13 17:08:50.443012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b96c6f2aabdb"
down_revision = "85b346bbd89e"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "client", "salesforce_id", existing_type=sa.String(length=45), nullable=True
    )


def downgrade():
    op.alter_column(
        "client", "salesforce_id", existing_type=sa.String(length=45), nullable=False
    )
