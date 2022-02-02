"""fix_analytics_heatstress_role

Revision ID: ccb6bc751210
Revises: baf99d48a7ee
Create Date: 2022-02-01 17:02:30.854263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ccb6bc751210"
down_revision = "baf99d48a7ee"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
            VALUES ('p', 'analytics_heatstress', 'analytics_heatstress', 'get')
        """
    )


def downgrade():
    op.execute(
        """
            DELETE FROM pipeline.casbin_rule
            WHERE v0 = 'analytics_heatstress' AND v1 = 'analytics_heatstress'
        """
    )
