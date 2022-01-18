"""rename_condition_table

Revision ID: e7ff0ada0d27
Revises: f36ba8ab8d50
Create Date: 2019-03-25 17:34:42.349303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e7ff0ada0d27"
down_revision = "f36ba8ab8d50"
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("condition", "rule_condition")
    pass


def downgrade():
    op.rename_table("rule_condition", "condition")
    pass
