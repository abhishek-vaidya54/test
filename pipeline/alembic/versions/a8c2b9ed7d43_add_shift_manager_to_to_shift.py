"""Add shift manager to to shift

Revision ID: a8c2b9ed7d43
Revises: d1afca2d2c01
Create Date: 2021-12-15 16:02:30.146104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a8c2b9ed7d43"
down_revision = "d1afca2d2c01"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("shifts", "group_administrator")

    op.add_column("shifts", sa.Column("shift_manager_id", sa.Integer, nullable=True))
    op.create_foreign_key(
        "fk_shifts_external_admin_user",
        "shifts",
        "external_admin_user",
        ["shift_manager_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("fk_shifts_external_admin_user", "shifts", "foreignkey")
    op.drop_column("shifts", "shift_manager_id")
    op.add_column("shifts", sa.Column("group_administrator", sa.String, nullable=True))
