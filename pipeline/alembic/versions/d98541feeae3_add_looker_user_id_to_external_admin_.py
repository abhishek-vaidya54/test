"""add_looker_user_id_to_external_admin_user

Revision ID: d98541feeae3
Revises: 7362f276939c
Create Date: 2021-01-18 15:01:58.321488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d98541feeae3"
down_revision = "c813aeef3940"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "external_admin_user",
        sa.Column("looker_user_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("external_admin_user", "looker_user_id")
