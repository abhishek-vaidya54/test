"""add shift job_function to admin

Revision ID: 1d714a7e2b53
Revises: d9c22c2126c3
Create Date: 2021-02-18 15:16:55.867683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1d714a7e2b53"
down_revision = "d9c22c2126c3"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            INSERT INTO pipeline.casbin_rule
                (ptype, v0, v1, v2)
            VALUES
                ('p', 'admin', 'shifts', 'post'),
                ('p', 'admin', 'shifts', 'put'),
                ('p', 'admin', 'jobfunctions', 'post'),
                ('p', 'admin', 'jobfunctions', 'put');
        """
    )


def downgrade():
    op.execute(
        """
            DELETE FROM pipeline.casbin_rule
            WHERE
                v0='admin'
            AND
                v1 IN ('shifts', 'jobfunctions')
            AND
                v2 IN ('post', 'put');
        """
    )
