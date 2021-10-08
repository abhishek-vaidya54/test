"""insert_looker_role_into_casbin_role

Revision ID: 8c13c1416d85
Revises: e3bccb6de746
Create Date: 2021-09-15 15:37:08.974544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c13c1416d85'
down_revision = 'e3bccb6de746'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    INSERT INTO pipeline.casbin_rule
        (ptype, v0, v1, v2)
    VALUES
        ("p", "looker", "looker", "get"),
        ("p", "looker", "looker", "post"),
        ("p", "looker", "looker", "put"),
        ("p", "looker", "looker", "delete");

    """
    )


def downgrade():
    op.execute(
        """
    DELETE FROM pipeline.casbin_rule WHERE v0='looker' AND v1='looker';
    
    """)
