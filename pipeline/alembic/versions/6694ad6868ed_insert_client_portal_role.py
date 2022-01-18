"""insert_client-portal_role

Revision ID: 6694ad6868ed
Revises: 8c13c1416d85
Create Date: 2021-09-30 13:47:08.604793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6694ad6868ed"
down_revision = "8c13c1416d85"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO pipeline.casbin_rule
            (ptype, v0, v1, v2)
        VALUES
            ("p", "client-portal", "client-portal", "get");
    """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM pipeline.casbin_rule WHERE v0='client-portal' AND v1='client-portal';
    """
    )
