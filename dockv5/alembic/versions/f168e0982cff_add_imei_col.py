"""add imei col

Revision ID: f168e0982cff
Revises: e79ea302e61f
Create Date: 2018-10-31 12:36:07.141055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f168e0982cff"
down_revision = "e79ea302e61f"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
      ALTER TABLE dockv5.config ADD COLUMN `dock_imei` VARCHAR(45) NULL DEFAULT NULL AFTER `dock_id` 
    """
    )


def downgrade():
    op.drop_column("config", "dock_imei")
