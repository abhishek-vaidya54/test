"""remove supervisor

Revision ID: 2f8b8f37c79a
Revises: 8be9b364cbda
Create Date: 2022-10-31 12:12:54.333224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f8b8f37c79a"
down_revision = "8be9b364cbda"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("fk_ia_external_admin_user", "industrial_athlete", "foreignkey")
    op.drop_column("industrial_athlete", "supervisor_id")
    op.drop_column("external_admin_user", "is_supervisor")
    op.drop_column("imported_industrial_athlete", "supervisor_id")


def downgrade():
    op.add_column(
        "industrial_athlete", sa.Column("supervisor_id", sa.Integer, nullable=True)
    )
    op.create_foreign_key(
        "fk_ia_external_admin_user",
        "industrial_athlete",
        "external_admin_user",
        ["supervisor_id"],
        ["id"],
    )
    op.add_column(
        "external_admin_user",
        sa.Column("is_supervisor", sa.Boolean(), nullable=True, server_default="0"),
    )
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("supervisor_id", sa.Integer(), nullable=True),
    )
