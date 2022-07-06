"""added extra salesforce field zoom industry info

Revision ID: 170232295d4f
Revises: 742b458bf73f
Create Date: 2022-07-06 11:05:22.515872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "170232295d4f"
down_revision = "742b458bf73f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column(
            "zoom_info_industry",
            sa.String(length=255),
            nullable=True,
        ),
    )
    op.alter_column(
        "client", "sub_pillar", existing_type=sa.String(length=255), nullable=True
    )


def downgrade():
    op.drop_column("client", "zoom_info_industry")
    op.alter_column(
        "client", "sub_pillar", existing_type=sa.String(length=45), nullable=True
    )
