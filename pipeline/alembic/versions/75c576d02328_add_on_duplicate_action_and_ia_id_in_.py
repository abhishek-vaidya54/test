"""add on_duplicate_action and ia_id in imported_imported_industrial_athlete

Revision ID: 75c576d02328
Revises: f2d0e56105a8
Create Date: 2020-10-19 15:31:34.323187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "75c576d02328"
down_revision = "f2d0e56105a8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "imported_industrial_athlete",
        sa.Column(
            "on_duplicate_action",
            sa.Enum("deactivate_and_insert", "update"),
            nullable=True,
        ),
    )
    op.add_column(
        "imported_industrial_athlete",
        sa.Column("ia_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("imported_industrial_athlete", "on_duplicate_action")
    op.drop_column("imported_industrial_athlete", "ia_id")
