"""add_superuser_and_admin_to_analytics_heatStress

Revision ID: baf99d48a7ee
Revises: 64d93c591fef
Create Date: 2022-01-20 16:18:24.834072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "baf99d48a7ee"
down_revision = "64d93c591fef"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
        VALUES
            ('p', 'superuser', 'analytics_heatStress', 'get'),
            ('p', 'admin', 'analytics_heatStress', 'get')
    """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM pipeline.casbin_rule
        WHERE v1 = 'analytics_heatStress' AND (v0 = 'superuser' OR v0 = 'admin')
    """
    )
