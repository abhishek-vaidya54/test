"""fix_casbin

Revision ID: c4ef1cb35597
Revises: ba12aaeed224
Create Date: 2022-01-04 14:43:57.711874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ef1cb35597'
down_revision = 'ba12aaeed224'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1)
        SELECT 'g', external_admin_user_id, role
        FROM pipeline.user_role_association
    """)

    op.execute("""
        INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2)
        VALUES ('p', 'bulk_upload', 'bulkupload', 'patch')
    """)


def downgrade():
    pass
