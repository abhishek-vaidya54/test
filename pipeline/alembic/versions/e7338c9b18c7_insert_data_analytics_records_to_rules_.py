"""insert data_analytics records to rules casbin

Revision ID: e7338c9b18c7
Revises: 2cdbc1d28383
Create Date: 2021-10-07 16:36:55.183137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e7338c9b18c7"
down_revision = "2cdbc1d28383"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    INSERT INTO pipeline.casbin_rule
        (ptype, v0, v1, v2)
    VALUES
        ("p", "data_analytics", "data_analytics", "get"),
        ("p", "data_analytics", "data_analytics", "post"),
        ("p", "data_analytics", "data_analytics", "put"),
        ("p", "data_analytics", "data_analytics", "delete");

    """
    )


def downgrade():
    op.execute(
        """
    DELETE FROM pipeline.casbin_rule WHERE v0='data_analytics' AND v1='data_analytics';
    
    """
    )
