"""add_superuser_and_admin_to_shift_manager_access

Revision ID: 4a9c7a8483d9
Revises: 3dcf0a8cc2cc
Create Date: 2021-12-17 17:37:53.139960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a9c7a8483d9'
down_revision = '3dcf0a8cc2cc'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
        VALUES
            ('p', 'superuser', 'shift_manager', 'get'),
            ('p', 'admin', 'shift_manager', 'get')
    """)


def downgrade():
    op.execute("""
        DELETE FROM pipeline.casbin_rule
        WHERE v1 = 'shift_manager' AND (v0 = 'superuser' OR v0 = 'admin')
    """)
