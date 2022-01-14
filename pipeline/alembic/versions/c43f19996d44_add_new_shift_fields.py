"""add_new_shift_fields

Revision ID: c43f19996d44
Revises: 83085a7d758c
Create Date: 2020-07-21 23:28:08.190768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c43f19996d44"
down_revision = "83085a7d758c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "shifts",
        sa.Column("timezone", sa.String(length=30), nullable=False),
    )


def downgrade():
    op.drop_column("shifts", "timezone")
