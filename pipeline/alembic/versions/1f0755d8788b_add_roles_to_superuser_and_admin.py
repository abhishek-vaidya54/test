"""add roles to superuser and admin

Revision ID: 1f0755d8788b
Revises: 3ecff42685c0
Create Date: 2022-09-22 21:07:12.967480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1f0755d8788b"
down_revision = "3ecff42685c0"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            INSERT INTO pipeline.casbin_rule
                (ptype, v0, v1, v2)
            VALUES
                ('p', 'superuser', 'looker_ergo', 'get'),
                ('p', 'superuser', 'looker_ergo', 'post'),
                ('p', 'superuser', 'looker_ergo', 'put'),
                ('p', 'superuser', 'looker_ergo', 'delete'),

                ('p', 'superuser', 'looker_prox', 'get'),
                ('p', 'superuser', 'looker_prox', 'post'),
                ('p', 'superuser', 'looker_prox', 'put'),
                ('p', 'superuser', 'looker_prox', 'delete'),

                ('p', 'superuser', 'analytics_heatstress', 'get'),
                ('p', 'superuser', 'analytics_heatstress', 'post'),
                ('p', 'superuser', 'analytics_heatstress', 'put'),
                ('p', 'superuser', 'analytics_heatstress', 'delete'),


                ('p', 'admin', 'looker_ergo', 'get'),
                ('p', 'admin', 'looker_ergo', 'post'),
                ('p', 'admin', 'looker_ergo', 'put'),
                ('p', 'admin', 'looker_ergo', 'delete'),

                ('p', 'admin', 'looker_prox', 'get'),
                ('p', 'admin', 'looker_prox', 'post'),
                ('p', 'admin', 'looker_prox', 'put'),
                ('p', 'admin', 'looker_prox', 'delete'),

                ('p', 'admin', 'analytics_heatstress', 'get'),
                ('p', 'admin', 'analytics_heatstress', 'post'),
                ('p', 'admin', 'analytics_heatstress', 'put'),
                ('p', 'admin', 'analytics_heatstress', 'delete');
                
        """
    )


def downgrade():
    op.execute(
        """
            DELETE FROM pipeline.casbin_rule
            WHERE
                v0 IN ('superuser', 'admin')
            AND
                v1 IN ('looker_ergo', 'looker_prox', 'analytics_heatstress')
            AND
                v2 IN ('get', 'post', 'put', 'delete');
        """
    )
