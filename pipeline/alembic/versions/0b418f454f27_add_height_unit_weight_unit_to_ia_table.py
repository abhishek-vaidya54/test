"""add height_unit weight_unit to ia table

Revision ID: 0b418f454f27
Revises: 49b9eef8f528
Create Date: 2020-12-15 15:21:49.033659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b418f454f27"
down_revision = "49b9eef8f528"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column(
            "ia_height_unit",
            sa.Enum("INCH", "CM"),
            server_default="INCH",
            nullable=False,
        ),
    ),
    op.add_column(
        "client",
        sa.Column(
            "ia_weight_unit",
            sa.Enum("LBS", "KG"),
            server_default="LBS",
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("client", "ia_height_unit")
    op.drop_column("client", "ia_weight_unit")
