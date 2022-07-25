"""add_supervisor_id_in_industrial_athlete

Revision ID: 8fd6a7a1336c
Revises: ed17a3e6fce9
Create Date: 2022-07-25 15:24:58.064569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8fd6a7a1336c"
down_revision = "ed17a3e6fce9"
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    op.drop_constraint("fk_ia_external_admin_user", "industrial_athlete", "foreignkey")
    op.drop_column("industrial_athlete", "supervisor_id")
