"""add post,put,delete roles for analytics_heatstress

Revision ID: 3ecff42685c0
Revises: 510598f20cf5
Create Date: 2022-09-21 17:27:10.909383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3ecff42685c0"
down_revision = "510598f20cf5"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            INSERT INTO pipeline.casbin_rule
                (ptype, v0, v1, v2)
            VALUES
                ('p', 'analytics_heatstress', 'analytics_heatstress', 'post'),
                ('p', 'analytics_heatstress', 'analytics_heatstress', 'put'),
                ('p', 'analytics_heatstress', 'analytics_heatstress', 'delete');
        """
    )


def downgrade():
    op.execute(
        """
            DELETE FROM pipeline.casbin_rule
            WHERE
                v0='analytics_heatstress'
            AND
                v1='analytics_heatstress'
            AND
                v2 IN ('post', 'put', 'delete');
        """
    )
