"""add show_ex_id_in_app to client

Revision ID: 86bc75340eb7
Revises: dfc30fb88fee
Create Date: 2020-12-23 14:30:55.906520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "86bc75340eb7"
down_revision = "dfc30fb88fee"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column("show_ex_id_in_app", sa.Boolean(), nullable=True, server_default="0"),
    )


def downgrade():
    op.drop_column("client", "show_ex_id_in_app")
