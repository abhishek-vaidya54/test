"""add-trigger_in_settings_table

Revision ID: 06799cabd257
Revises: 75e5f7db0893
Create Date: 2021-08-10 17:17:31.870732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06799cabd257"
down_revision = "75e5f7db0893"
branch_labels = None
depends_on = None


def upgrade():
    trigger = """
                CREATE TRIGGER disallow_modify BEFORE UPDATE ON settings
                FOR EACH ROW
                BEGIN
                    signal sqlstate '45000' set message_text = 'Update Not Allowed on this table';
                END;
            """
    op.execute(trigger)
    pass


def downgrade():
    op.execute("drop trigger if exists disallow_modify;")
    pass