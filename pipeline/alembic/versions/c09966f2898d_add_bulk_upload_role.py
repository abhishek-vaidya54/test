"""add bulk_upload role

Revision ID: c09966f2898d
Revises: 829cef4e1165
Create Date: 2020-12-28 12:17:29.637811

"""
from alembic import op
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "c09966f2898d"
down_revision = "829cef4e1165"
branch_labels = None
depends_on = None

actions = ["get", "put", "post", "delete"]


def upgrade():

    op.execute('DELETE FROM pipeline.casbin_rule where v1="bulkupload"')

    op.execute(
        """
        INSERT INTO pipeline.user_role_association (external_admin_user_id, role, db_created_at, db_modified_at)
        SELECT external_admin_user_id, "bulk_upload", "{0}", "{0}" 
        FROM pipeline.user_role_association
        where role="superuser" or role="admin"
        """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )

    for action in actions:
        op.execute(
            'INSERT INTO pipeline.casbin_rule (ptype, v0, v1, v2) VALUES ("p", "bulk_upload", "bulkupload", "{}")'.format(
                action
            )
        )


def downgrade():
    op.execute('DELETE FROM pipeline.casbin_rule WHERE v0="bulk_upload"')
   
    op.execute(
        'DELETE FROM pipeline.user_role_association WHERE role="bulk_upload"'
    )
