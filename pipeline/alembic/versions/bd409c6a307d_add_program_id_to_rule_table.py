"""add_program_id_to_rule_table

Revision ID: bd409c6a307d
Revises: 423f4e59eb62
Create Date: 2019-05-01 00:07:54.192569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd409c6a307d"
down_revision = "423f4e59eb62"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("rule", sa.Column("program_id", sa.Integer(), nullable=True))
    pass


def downgrade():
    op.drop_column("rule", "program_id")
    pass
