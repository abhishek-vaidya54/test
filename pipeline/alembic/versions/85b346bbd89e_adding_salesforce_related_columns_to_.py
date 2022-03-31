"""adding_salesforce_related_columns_to_client_table

Revision ID: 85b346bbd89e
Revises: 60004256e42a
Create Date: 2022-03-31 18:13:41.616035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "85b346bbd89e"
down_revision = "60004256e42a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "client",
        sa.Column(
            "salesforce_id",
            sa.String(length=45),
            nullable=False,
        ),
    )
    op.add_column(
        "client",
        sa.Column(
            "vertical",
            sa.String(length=45),
            nullable=True,
        ),
    )
    op.add_column(
        "client",
        sa.Column(
            "sub_pillar",
            sa.String(length=45),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("client", "salesforce_id")
    op.drop_column("client", "vertical")
    op.drop_column("client", "sub_pillar")
