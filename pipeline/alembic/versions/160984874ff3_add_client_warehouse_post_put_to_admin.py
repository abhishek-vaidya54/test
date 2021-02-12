"""add_client_warehouse_post_put_to_admin

Revision ID: 160984874ff3
Revises: 955a49ff7c9e
Create Date: 2021-02-04 14:32:09.935803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "160984874ff3"
down_revision = "955a49ff7c9e"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            INSERT INTO pipeline.casbin_rule
                (ptype, v0, v1, v2)
            VALUES
                ('p', 'admin', 'clients', 'post'),
                ('p', 'admin', 'clients', 'put'),
                ('p', 'admin', 'warehouses', 'post'),
                ('p', 'admin', 'warehouses', 'put');
        """
    )


def downgrade():
    op.execute(
        """
            DELETE FROM pipeline.casbin_rule
            WHERE
                v0='admin'
            AND
                v1 IN ('clients', 'warehouses')
            AND
                v2 IN ('post', 'put');
        """
    )
