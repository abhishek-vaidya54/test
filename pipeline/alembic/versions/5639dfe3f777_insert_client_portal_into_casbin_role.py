"""insert_client_portal_into_casbin_role

Revision ID: 5639dfe3f777
Revises: 8c13c1416d85
Create Date: 2021-09-22 14:00:40.963468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5639dfe3f777'
down_revision = '8c13c1416d85'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO pipeline.casbin_rule
            (ptype, v0, v1, v2)
        VALUES
            ("p", "client-portal", "client-portal", "get");
    """)


def downgrade():
    op.execute("""
        DELETE FROM pipeline.casbin_rule WHERE v0='looker' AND v1='looker';
    """)
