"""adding_salesforce_id_column_to_client

Revision ID: b80431d2fe9e
Revises: ccb6bc751210
Create Date: 2022-03-07 11:37:35.105807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b80431d2fe9e'
down_revision = 'ccb6bc751210'
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


def downgrade():
    op.drop_column("client", "salesforce_id")
