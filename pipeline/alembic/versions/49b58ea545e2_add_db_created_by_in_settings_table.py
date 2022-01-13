"""Add db_created_by in settings table

Revision ID: 49b58ea545e2
Revises: f5641c61905a
Create Date: 2021-07-05 15:19:59.824143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "49b58ea545e2"
down_revision = "f5641c61905a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "settings",
        sa.Column("db_created_by", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_settings_user", "settings", "external_admin_user", ["db_created_by"], ["id"]
    )


def downgrade():
    op.drop_constraint("fk_settings_user", "settings", "foreignkey")
    op.drop_column("settings", "db_created_by")
