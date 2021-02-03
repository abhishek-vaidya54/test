"""update_app_restart_at_type_to_warehouse_table

Revision ID: 955a49ff7c9e
Revises: 0dfec63dee9c
Create Date: 2021-02-01 14:44:43.616419

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = "955a49ff7c9e"
down_revision = "0dfec63dee9c"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("warehouse", "app_restart_at")
    op.add_column(
        "warehouse",
        sa.Column(
            "app_restart_at",
            sa.TIME(),
            server_default=str(
            datetime.datetime.now().replace(hour=0, minute=0, second=0).strftime("%H:%M:%S")
            ),
            nullable=False,
        ),
    )


def downgrade():    
    pass
    #Todo: If we want to remove this migration we need to specificly add here as its an alteration of existing migration, we have to fix this whenever we re-migrate everything.